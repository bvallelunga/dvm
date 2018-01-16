clis = [
  require "./wallet"
]

module.exports.init = (program)->
  for cli in clis 
    cli.init(program)