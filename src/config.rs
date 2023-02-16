use std::collections::HashMap;
use std::fs::read_to_string;

use regex::Regex;
use serde::{
    Deserialize,
    Serialize,
};

use super::{
    Action,
    CommandMatcher,
    ConfigErrors,
    Matcher,
    MessageAction,
    RegExMatcher,
};

pub trait ConfigMatcher {
    fn as_matcher(&self,);
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
pub struct ActionEntry {
    kind: String,
    args: HashMap<String, String,>,
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
pub struct MatcherEntry {
    kind: String,
    args: HashMap<String, String,>,
    action: ActionEntry,
}

fn make_action(
    kind: &str,
    args: &HashMap<String, String,>,
) -> Result<Box<dyn Action,>, ConfigErrors,> {
    match kind {
        "message" => {
            let template = match args.get("template",) {
                Some(value,) => value.clone(),
                _ => return Err(ConfigErrors::MissingValue,),
            };
            Ok(Box::new(MessageAction {
                template: template,
            },),)
        }
        _ => return Err(ConfigErrors::UnknownActionType,),
    }
}

fn make_matcher(
    matcher_kind: &str,
    matcher_args: &HashMap<String, String,>,
    action: Box<dyn Action,>,
) -> Result<Box<dyn Matcher,>, ConfigErrors,> {
    match matcher_kind {
        "regex" => {
            let rule = match matcher_args.get("rule",) {
                Some(value,) => value.clone(),
                _ => return Err(ConfigErrors::MissingValue,),
            };
            Ok(Box::new(RegExMatcher {
                regex: Regex::new(rule.as_str(),).unwrap(),
                to_lower: true,
                action: action,
            },),)
        }
        "command" => {
            let token = match matcher_args.get("token",) {
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
        _ => return Err(ConfigErrors::UnknownMatcherType,),
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
            make_action(&matcher_entry.action.kind, &matcher_entry.action.args,)?;
        let matcher = make_matcher(&matcher_entry.kind, &matcher_entry.args, action,)?;
        results.push(matcher,);
    }
    Ok(results,)
}
