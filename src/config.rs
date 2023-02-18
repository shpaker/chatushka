use std::collections::HashMap;
use std::fs::read_to_string;

use regex::Regex;
use rhai::{
    Engine,
    EvalAltResult,
};
use serde::{
    Deserialize,
    Serialize,
};

use super::{
    Action,
    MessageAction,
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

use super::{
    CommandMatcher,
    ConfigErrors,
    Matcher,
    RegExMatcher,
};

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
pub struct ActionEntry {
    kind: ActionsKind,
    args: HashMap<String, String,>,
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
pub struct MatcherEntry {
    kind: MatchersKind,
    args: HashMap<String, String,>,
    action: ActionEntry,
}

fn make_action(
    kind: ActionsKind,
    args: &HashMap<String, String,>,
) -> Result<Box<dyn Action,>, ConfigErrors,> {
    match kind {
        ActionsKind::Message => {
            let template = match args.get("template",) {
                Some(value,) => value.clone(),
                _ => return Err(ConfigErrors::MissingValue,),
            };
            Ok(Box::new(MessageAction {
                template: template,
            },),)
        }
        ActionsKind::Rhai => {
            let script = match args.get("script",) {
                Some(value,) => value.clone(),
                _ => return Err(ConfigErrors::MissingValue,),
            };
            Ok(Box::new(RhaiAction { script: script, },),)
        }
    }
}

fn make_matcher(
    kind: MatchersKind,
    args: &HashMap<String, String,>,
    action: Box<dyn Action,>,
) -> Result<Box<dyn Matcher,>, ConfigErrors,> {
    match kind {
        MatchersKind::RegEx => {
            let rule = match args.get("rule",) {
                Some(value,) => value.clone(),
                _ => return Err(ConfigErrors::MissingValue,),
            };
            Ok(Box::new(RegExMatcher {
                regex: Regex::new(rule.as_str(),).unwrap(),
                to_lower: true,
                action,
            },),)
        }
        MatchersKind::Command => {
            let token = match args.get("token",) {
                Some(value,) => value.clone(),
                _ => return Err(ConfigErrors::MissingValue,),
            };
            Ok(Box::new(CommandMatcher {
                token,
                case_insensitive: true,
                prefixes: vec!['!', 'z'],
                action,
            },),)
        }
        _ => {
            let token = match args.get("token",) {
                Some(value,) => value.clone(),
                _ => return Err(ConfigErrors::MissingValue,),
            };
            Ok(Box::new(CommandMatcher {
                token,
                case_insensitive: true,
                prefixes: vec!['!', 'z'],
                action,
            },),)
        }
    }
}

pub fn read_config(path: &str,) -> Result<Vec<Box<dyn Matcher,>,>, ConfigErrors,> {
    let yaml = match read_to_string(path,) {
        Ok(yaml,) => yaml,
        Err(_err,) => return Err(ConfigErrors::MissingValue,),
    };
    let mut results: Vec<Box<dyn Matcher,>,> = Vec::new();
    for doc in serde_yaml::Deserializer::from_str(yaml.as_str(),) {
        let matcher_entry = MatcherEntry::deserialize(doc,).unwrap();
        let action =
            make_action(matcher_entry.action.kind, &matcher_entry.action.args,)?;
        let matcher = make_matcher(matcher_entry.kind, &matcher_entry.args, action,)?;
        results.push(matcher,);
    }
    Ok(results,)
}
