use super::{
    BotAPI,
    BotErrors,
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

pub struct ChatListener<'a,> {
    api: BotAPI,
    matchers: &'a Vec<RegExMatcher,>,
}

impl ChatListener<'_,> {
    pub fn new<'a,>(
        token: &'a str,
        matchers: &'a Vec<RegExMatcher,>,
    ) -> ChatListener<'a,> {
        ChatListener {
            api: BotAPI::new(token,),
            matchers: matchers,
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
            messages.push(Message {
                id: entry_json["message"]["message_id"].as_i64().unwrap(),
                update_id: entry_json["update_id"].as_i64().unwrap(),
                chat_id: entry_json["message"]["chat"]["id"].as_i64().unwrap(),
                text: entry_json["message"]["text"].as_str().unwrap().to_string(),
            },);
        }
        return Ok(messages,);
    }

    pub fn long_polling(&self,) -> Result<(), BotErrors,> {
        let mut massages = self.get_message_updates(None, 16,)?;
        let mut next_update_id = get_latest_update_id(&massages,) + 1;
        loop {
            massages = self.get_message_updates(Some(next_update_id,), 60,)?;
            if massages.len() == 0 {
                continue;
            }
            next_update_id = get_latest_update_id(&massages,) + 1;
            for massage in massages.into_iter() {
                for matcher in self.matchers.into_iter() {
                    matcher.check(&self.api, &massage,);
                }
            }
        }
    }
}
