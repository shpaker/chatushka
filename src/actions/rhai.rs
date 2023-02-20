use log::warn;
use rhai::{
    Engine,
    Scope,
    AST,
};

use super::Action;
use crate::{
    ListenerErrors,
    Message,
    TelegramAPI,
};

pub struct RhaiAction {
    pub script: AST,
    pub entrypoint: Option<String,>,
}

impl RhaiAction {
    pub fn new(
        script: &str,
        entrypoint: Option<String,>,
        engine: &Engine,
    ) -> Result<RhaiAction, ListenerErrors,> {
        let script = match engine.compile(script,) {
            Ok(script,) => script,
            Err(_err,) => return Err(ListenerErrors::CompileError,),
        };
        Ok(RhaiAction {
            script, entrypoint,
        },)
    }
}

impl Action for RhaiAction {
    fn call(
        &self,
        api: &TelegramAPI,
        message: &Message,
        rhai_engine: &Engine,
    ) -> Result<(), ListenerErrors,> {
        let mut scope = Scope::new();
        scope
            .push_constant("CHAT_ID", message.chat_id,)
            .push_constant("MESSAGE_ID", message.id,)
            .push_constant("MESSAGE_TEXT", message.text.clone(),);
        let mut result: Option<String,> = None;
        match &self.entrypoint {
            None => {
                match rhai_engine.eval_ast_with_scope(&mut scope, &self.script,) {
                    Ok(message,) => result = Some(message,),
                    Err(_err,) => {
                        warn!("error {:?}", { _err });
                        return Err(ListenerErrors::CallActionError,);
                    }
                };
            }
            Some(value,) => {
                match rhai_engine.call_fn::<String>(
                    &mut scope,
                    &self.script,
                    value,
                    (),
                ) {
                    Ok(message,) => result = Some(message,),
                    Err(_err,) => {
                        warn!("error {:?}", { _err });
                        return Err(ListenerErrors::CallActionError,);
                    }
                };
            }
        };
        if result == None {
            return Ok((),);
        } else {
            api.send_message(
                message.chat_id,
                result.unwrap().as_str(),
                message.id,
                16,
            );
        }
        Ok((),)
    }
}
