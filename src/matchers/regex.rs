use regex::Regex;
use rhai::Engine;

use super::Matcher;
use crate::{
    Action,
    BotAPI,
    Message,
};

pub struct RegExMatcher {
    pub regex: Regex,
    pub to_lower: bool,
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
        rhai_engine: &Engine,
    ) {
        self.action.call(api, message, &rhai_engine,);
    }
}
