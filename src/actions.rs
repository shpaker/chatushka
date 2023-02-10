use super::{
    BotAPI,
    Message,
};

pub trait Action {
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
    );
}

pub struct MessageAction {
    pub template: &'static str,
}

impl Action for MessageAction {
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
    ) {
        let result = api.send_message(message.chat_id, self.template, message.id, 16,);
        result.ok();
    }
}
