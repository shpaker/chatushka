use serde_json::Value;

use super::{
    BotAPI,
    Matcher,
    Message,
};
use crate::matcher::RegExMatcher;

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

#[derive(Debug,)]
pub struct ChatListener<'a,> {
    api: BotAPI,
    matchers: &'a Vec<RegExMatcher,>,
}

impl ChatListener<'_,> {
    pub fn new<'a,>(
        token: &str,
        matchers: &'a Vec<RegExMatcher,>,
    ) -> ChatListener<'a,> {
        for matcher in matchers {
            println!("{:#?}", matcher);
        }
        ChatListener {
            api: BotAPI::new(token,),
            matchers: matchers,
        }
    }

    pub fn get_message_updates(
        &self,
        offset: Option<i64,>,
        timeout: u64,
    ) -> Option<Vec<Message,>,> {
        let response = self.api.get_updates(offset, timeout,);
        if response.is_none() {
            return None;
        }
        let mut messages: Vec<Message,> = Vec::new();
        for entry in response.unwrap().as_array().unwrap() {
            let entry_map = entry.as_object();
            if entry_map.is_none() {
                continue;
            }
            let messages_json = entry_map.unwrap();
            if messages_json["message"]["text"] == Value::Null {
                continue;
            }
            messages.push(Message {
                id: messages_json["message"]["message_id"]
                    .as_i64()
                    .unwrap(),
                update_id: messages_json["update_id"].as_i64().unwrap(),
                chat_id: messages_json["message"]["chat"]["id"]
                    .as_i64()
                    .unwrap(),
                text: messages_json["message"]["text"]
                    .as_str()
                    .unwrap()
                    .to_string(),
            },);
        }
        return Some(messages,);
    }

    pub fn long_polling(&self,) {
        let mut updates = self.get_message_updates(None, 16,);
        let mut latest_update_id =
            get_latest_update_id(&updates.unwrap(),);
        loop {
            updates = self
                .get_message_updates(Some(latest_update_id + 1,), 60,);
            if updates.is_none() {
                continue;
            }
            let unwrapped = updates.unwrap();
            if unwrapped.len() == 0 {
                continue;
            }
            latest_update_id = get_latest_update_id(&unwrapped,);
            for massage in unwrapped.into_iter() {
                for matcher in self.matchers.into_iter() {
                    matcher.check(&self.api, &massage,);
                }
            }
        }
    }
}
