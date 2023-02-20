use rhai::Engine;

use crate::{
    ListenerErrors,
    Message,
    TelegramAPI,
};

pub trait Action {
    fn call(
        &self,
        api: &TelegramAPI,
        message: &Message,
        rhai_engine: &Engine,
    ) -> Result<(), ListenerErrors,>;
}
