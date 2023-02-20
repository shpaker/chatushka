use rhai::Engine;

use crate::{
    Action,
    ListenerErrors,
    Message,
    TelegramAPI,
};

pub struct MessageAction {
    pub template: String,
}

impl Action for MessageAction {
    fn call(
        &self,
        api: &TelegramAPI,
        message: &Message,
        _rhai_engine: &Engine,
    ) -> Result<(), ListenerErrors,> {
        match api
            .send_message(message.chat_id, self.template.as_str(), message.id, 16,)
        {
            Ok(_result,) => (),
            Err(_err,) => return Err(ListenerErrors::CallActionError,),
        };
        Ok((),)
    }
}
