import { DiscordClient } from "./DiscordClient.js"

const App = () => {
  const args = {
    'discord_token_file_path': 'keys/discord_token.json',
    'ost_file_path': 'data/ost_list.json'
  }

  const discord_cli = new DiscordClient(args)
}

export {
  App
}