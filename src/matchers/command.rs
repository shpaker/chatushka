use super::Matcher;
use crate::Message;

pub struct CommandMatcher {
    pub token: String,
    pub case_insensitive: bool,
    pub prefixes: Vec<char,>,
}

impl Matcher for CommandMatcher {
    fn is_match(
        &self,
        message: &Message,
    ) -> bool {
        message.text.starts_with(&self.token,)
    }
}
