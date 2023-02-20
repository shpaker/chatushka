use regex::Regex;

use super::Matcher;
use crate::Message;

pub struct RegExMatcher {
    pub regex: Regex,
    pub to_lower: bool,
}

impl Matcher for RegExMatcher {
    fn is_match(
        &self,
        message: &Message,
    ) -> bool {
        self.regex.is_match(message.text.as_str(),)
    }
}
