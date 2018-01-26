#!/usr/bin/env coffee
program = require("commander")
config = require("./package")
commands = require("./cli")


# Set Program
program
  .description(config.description)
  .version(config.version)
 
  
# Load Commands 
commands.init(program)
program.parse(process.argv)
  
  
# Print Help
if program.args.length == 0
  console.log(program.help())