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

        let ast = rhai_engine.compile(&self.script,).unwrap();
        let result = match rhai_engine.call_fn::<String>(
            &mut scope,
            &ast,
            self.entrypoint.as_str(),
            (),
        ) {
            Ok(message,) => message,
            Err(_err,) => return println!("{:?}", _err),
        };
        println!("{:?}", result);
        let response = result;
        // let response = match result {
        //     None => return (),
        //     Some(response) => response,
        // };
        println!("{:?}", response);
        api.send_message(message.chat_id, response.as_str(), message.id, 16,);
    }
}
