use super::Matcher;
use crate::{
    Action,
    BotAPI,
    Message,
};

pub struct CommandMatcher {
    pub token: String,
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
