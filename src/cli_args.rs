use clap::Parser;

#[derive(Parser, Debug,)]
#[command(author, version, about, long_about = None)]
pub struct CliArgs {
    #[arg(short, long)]
    pub token: String,
    #[arg(short, long, action)]
    pub debug: bool,
    #[arg(short, long)]
    pub config: String,
}
