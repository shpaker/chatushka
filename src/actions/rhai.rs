use rhai::{
    Engine,
    EvalAltResult,
};

use crate::bot::Message;
use crate::Action;
use crate::BotAPI;

pub struct RhaiAction {
    pub script: String,
}

impl Action for RhaiAction {
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
        rhai_engine: &Engine,
    ) {
        rhai_engine.run(self.script.as_str(),);
    }
}
