use std::{
    thread,
    time,
};

use log::info;
use rhai::{
    packages::Package,
    Engine,
};
use rhai_fs::FilesystemPackage;
use rhai_rand::RandomPackage;

use super::{
    Message,
    TelegramAPI,
};
use crate::{
    BotErrors,
    Listener,
};

fn get_latest_update_id(messages: &Vec<Message,>,) -> i64 {
    let mut latest_update_id: i64 = 0;
    for message in messages.into_iter() {
        if latest_update_id == 0 {
            latest_update_id = message.update_id;
            continue;
        }
        if message.update_id > latest_update_id {
            latest_update_id = message.update_id;
        }
    }
    return latest_update_id;
}

pub struct Bot {
    api: TelegramAPI,
    pub rhai_engine: Engine,
}

impl Bot {
    pub fn new(token: &str,) -> Bot {
        let mut rhai_engine = Engine::new();
        rhai_engine.register_global_module(RandomPackage::new().as_shared_module(),);
        let package = FilesystemPackage::new();
        package.register_into_engine(&mut rhai_engine,);
        Bot {
            api: TelegramAPI::new(token,),
            rhai_engine,
        }
    }

    fn get_message_updates(
        &self,
        offset: Option<i64,>,
        timeout: u64,
    ) -> Result<Vec<Message,>, BotErrors,> {
        let response = self.api.get_updates(offset, timeout,)?;
        let mut messages: Vec<Message,> = Vec::new();
        for entry in response.as_array().unwrap() {
            let entry_json = match entry.as_object() {
                None => continue,
                Some(entry_map,) => entry_map,
            };
            if entry_json.get("message",) == None {
                continue;
            }
            if entry_json["message"].get("text",) == None {
                continue;
            }
            messages.push(Message {
                id: entry_json["message"]["message_id"].as_i64().unwrap(),
                update_id: entry_json["update_id"].as_i64().unwrap(),
                chat_id: entry_json["message"]["chat"]["id"].as_i64().unwrap(),
                text: entry_json["message"]["text"].as_str().unwrap().to_string(),
            },);
        }
        return Ok(messages,);
    }

    fn process_incoming_messages(
        &self,
        messages: &Vec<Message,>,
        listeners: &Vec<Listener,>,
    ) {
        for message in messages.into_iter() {
            for listener in listeners.iter() {
                if listener.matcher.is_match(&message,) {
                    match listener
                        .action
                        .call(&self.api, &message, &self.rhai_engine,)
                    {
                        Ok(_,) => {
                            info!("action matched!");
                        }
                        Err(err,) => {
                            info!("action err: {:?}", err);
                        }
                    };
                };
            }
        }
    }

    fn long_polling(
        &self,
        listeners: &Vec<Listener,>,
    ) -> Result<(), BotErrors,> {
        let delay = time::Duration::from_secs(2,);
        let mut massages = self.get_message_updates(None, 16,)?;
        let mut next_update_id = get_latest_update_id(&massages,) + 1;
        loop {
            massages = match self.get_message_updates(Some(next_update_id,), 60,) {
                Err(err,) => {
                    info!("get updates err: {:?}", err);
                    thread::sleep(delay,);
                    continue;
                }
                Ok(value,) => value,
            };
            if massages.len() == 0 {
                thread::sleep(delay,);
                continue;
            }
            next_update_id = get_latest_update_id(&massages,) + 1;
            self.process_incoming_messages(&massages, listeners,);
            thread::sleep(delay,);
        }
    }

    pub fn run(
        &self,
        listeners: &Vec<Listener,>,
    ) -> Result<(), BotErrors,> {
        self.long_polling(listeners,)
    }
}
