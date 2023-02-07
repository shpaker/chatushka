use std::collections::HashMap;

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
    // fn check_config(
    //     &self,
    //     config: HashMap<String, String>,
    // );
    // fn from_config(
    //     &self,
    //     config: HashMap<String, String>,
    // );
}

pub struct RegExMatcher {
    regex: Regex,
    cb: fn(&BotAPI, &Message,),
}

impl RegExMatcher {
    pub fn new(
        regex: &str,
        cb: fn(&BotAPI, &Message,),
    ) -> RegExMatcher {
        RegExMatcher {
            regex: Regex::new(regex,).unwrap(),
            cb: cb,
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
            (self.cb)(api, message,);
        }
    }
}
