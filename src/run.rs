use super::{
    ChatListener,
    Settings,
};
use crate::matcher::RegExMatcher;

pub fn run() {
    let config = Settings::new();
    let matchers = vec![RegExMatcher::new(r"^(test).*$",)];
    let listener =
        ChatListener::new(config.bot_token.as_str(), &matchers,);
    listener.long_polling();
}
