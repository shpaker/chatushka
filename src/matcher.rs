use regex::Regex;

use super::{
    Action,
    BotAPI,
    Message,
};

pub trait Matcher {
    fn is_check(
        &self,
        message: &Message,
    ) -> bool;
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
    );
}

pub struct RegExMatcher {
    pub regex: Regex,
    pub case_insensitive: bool,
    pub action: Box<dyn Action,>,
}

impl Matcher for RegExMatcher {
    fn is_check(
        &self,
        message: &Message,
    ) -> bool {
        self.regex.is_match(message.text.as_str(),)
    }
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
    ) {
        self.action.call(api, message,);
    }
}

pub struct CommandMatcher {
    pub token: &'static str,
    pub case_insensitive: bool,
    pub prefixes: Vec<char,>,
    pub action: Box<dyn Action,>,
}

impl Matcher for CommandMatcher {
    fn is_check(
        &self,
        message: &Message,
    ) -> bool {
        message.text.starts_with(&self.token,)
    }

    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
    ) {
        self.action.call(api, message,);
    }
}
