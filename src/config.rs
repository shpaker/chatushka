use std::collections::HashMap;
use std::error::Error;
use std::fs::read_to_string;

use serde::{
    Deserialize,
    Serialize,
};

pub trait ConfigMatcher {
    fn as_matcher(&self,);
}

pub struct ConfigRegExMatcher {
    kind: String,
    rule: String,
}

impl ConfigMatcher for ConfigRegExMatcher {
    fn as_matcher(&self,) {
        todo!()
    }
}

pub struct ConfigCommandMatcher {
    kind: String,
    command: String,
}

#[derive(Serialize, Deserialize, PartialEq, Debug,)]
pub struct RawConfigEntry {
    matcher: HashMap<String, String,>,
    action: HashMap<String, String,>,
}

pub fn read_config(path: &str,) -> Result<Vec<RawConfigEntry,>, Box<dyn Error,>,> {
    let yaml: String = read_to_string(path,)?;
    let entries: Vec<RawConfigEntry,> = serde_yaml::from_str(&yaml,).unwrap();
    println!("{:?}", entries);
    // for entry in entries {
    //     if entry.matcher
    // }
    Ok(entries,)
}
