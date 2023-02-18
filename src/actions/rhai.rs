use rhai::{
    Engine,
    Scope,
};

use crate::bot::Message;
use crate::Action;
use crate::BotAPI;

pub struct RhaiAction {
    pub script: String,
    pub entrypoint: String,
}

impl Action for RhaiAction {
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
        rhai_engine: &Engine,
    ) {
        let mut scope = Scope::new();
        scope
            .push_constant("CHAT_ID", message.chat_id,)
            .push_constant("MESSAGE_ID", message.id,)
            .push_constant("MESSAGE_TEXT", message.text.clone(),);
        let result = match rhai_engine
            .eval_with_scope::<String>(&mut scope, self.script.as_str(),)
        {
            Ok(message,) => message,
            Err(_err,) => return println!("{:?}", _err),
        };
        api.send_message(message.chat_id, result.as_str(), message.id, 16,);
    }
}
