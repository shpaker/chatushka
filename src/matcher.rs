use regex::Regex;

use super::{
    BotAPI,
    Message,
};

pub trait Matcher {
    fn check(
        &self,
        api: &BotAPI,
        message: &Message,
    );
}

#[derive(Debug,)]
pub struct RegExMatcher {
    regex: Regex,
}

impl RegExMatcher {
    pub fn new(regex: &str,) -> RegExMatcher {
        RegExMatcher {
            regex: Regex::new(regex,).unwrap(),
        }
    }
}

impl Matcher for RegExMatcher {
    fn check(
        &self,
        api: &BotAPI,
        message: &Message,
    ) {
        if self.regex.is_match(message.text.as_str(),) {
            api.send_message(message.chat_id, "wow", message.id, 16,);
        }
        // println!("{:?}", message.text);
        // println!("{:?}", a);
        // !found.is_none()
    }
}
