use std::collections::HashMap;
use std::env::args;
use std::fs::read_to_string;

use regex::Regex;
use rhai::Engine;
use serde::{
    Deserialize,
    Serialize,
};

use super::{
    Action,
    CommandMatcher,
    ConfigErrors,
    Listener,
    Matcher,
    MessageAction,
    RegExMatcher,
    RhaiAction,
};

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
#[serde(rename_all = "lowercase")]
enum MatchersKind {
    RegEx,
    Command,
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
#[serde(rename_all = "lowercase")]
enum ActionsKind {
    Message,
    Rhai,
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
struct ActionConfig {
    kind: ActionsKind,
    args: HashMap<String, String,>,
}

impl ActionConfig {
    fn to_action(
        &self,
        rhai_engine: &Engine,
    ) -> Result<Box<dyn Action,>, ConfigErrors,> {
        match self.kind {
            ActionsKind::Message => {
                let template = match self.args.get("template",) {
                    Some(value,) => value.clone(),
                    _ => return Err(ConfigErrors::MissingValue,),
                };
                Ok(Box::new(MessageAction {
                    template: template,
                },),)
            }
            ActionsKind::Rhai => {
                let script = match self.args.get("script",) {
                    Some(value,) => value.clone(),
                    _ => return Err(ConfigErrors::MissingValue,),
                };
                let entrypoint = match self.args.get("entrypoint",) {
                    Some(value,) => Some(value.clone(),),
                    None => None,
                };
                // .args
                // .get("entrypoint",)
                // .unwrap_or(&"main".to_string(),)
                // .clone();
                Ok(Box::new(
                    RhaiAction::new(&script.as_str(), entrypoint, rhai_engine,)
                        .unwrap(),
                ),)
            }
        }
    }
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
struct MatcherConfig {
    kind: MatchersKind,
    args: HashMap<String, String,>,
}

impl MatcherConfig {
    fn to_matcher(&self,) -> Result<Box<dyn Matcher,>, ConfigErrors,> {
        match self.kind {
            MatchersKind::RegEx => {
                let rule = match self.args.get("rule",) {
                    Some(value,) => value.clone(),
                    _ => return Err(ConfigErrors::MissingValue,),
                };
                Ok(Box::new(RegExMatcher {
                    regex: Regex::new(rule.as_str(),).unwrap(),
                    to_lower: true,
                },),)
            }
            MatchersKind::Command => {
                let token = match self.args.get("token",) {
                    Some(value,) => value.clone(),
                    _ => return Err(ConfigErrors::MissingValue,),
                };
                Ok(Box::new(CommandMatcher {
                    token,
                    case_insensitive: true,
                    prefixes: vec!['!', 'z'],
                },),)
            }
        }
    }
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
struct ListenerConfig {
    matcher: MatcherConfig,
    action: ActionConfig,
    data: Option<Vec<String,>,>,
}
impl ListenerConfig {
    fn to_listener(
        &self,
        rhai_engine: &Engine,
    ) -> Result<Listener, ConfigErrors,> {
        let data: Vec<String,> = self.data.clone().unwrap_or(Vec::new(),);
        Ok(Listener {
            matcher: self.matcher.to_matcher()?,
            action: self.action.to_action(rhai_engine,)?,
            data,
        },)
    }
}

pub struct Config {
    pub listeners: Vec<Listener,>,
}

impl Config {
    pub fn from_file(
        path: &str,
        rhai_engine: &Engine,
    ) -> Result<Config, ConfigErrors,> {
        let yaml = match read_to_string(path,) {
            Ok(yaml,) => yaml,
            Err(_err,) => return Err(ConfigErrors::MissingValue,),
        };
        let mut listeners: Vec<Listener,> = Vec::new();
        for doc in serde_yaml::Deserializer::from_str(yaml.as_str(),) {
            let listener_config = ListenerConfig::deserialize(doc,).unwrap();
            listeners.push(listener_config.to_listener(rhai_engine,)?,);
        }
        Ok(Config { listeners, },)
    }
}
