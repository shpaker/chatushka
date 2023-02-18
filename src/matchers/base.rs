use rhai::Engine;

use crate::{
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
        rhai_engine: &Engine,
    );
}
