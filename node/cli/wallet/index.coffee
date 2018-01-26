clis = {
  create: require "./create"
  load: require "./load"
}

module.exports.init = (program)->
  program
    .command('wallet')
    .description('Create or load your wallet address. This will act as your access-token and payout acount.')
    .option("-c, --create", "Create wallet address")
    .option("-l, --load", "Create wallet address")
    .action (env)->    
      if env.create
        clis.create(env)
        
      else if env.load
        clis.load(env)
        
      else 
        console.log env.help()