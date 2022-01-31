import { Constants, Client } from 'discord.js'
import { existsSync, readFileSync, writeFileSync } from 'fs'
import ytdl from 'ytdl-core'
import minimist from 'minimist';
import { parseArgsStringToArgv } from 'string-argv'

const _DISCORD_PREFIX = "?"

class DiscordClient {
	constructor(args) {
    this.client = new Client()

    this.client.on(Constants.Events.CLIENT_READY, this._on_discord_ready)
    this.client.on(Constants.Events.MESSAGE_CREATE, this._on_discord_message)

    this.ost_file_path = args.ost_file_path
    this.ost = JSON.parse(readFileSync(this.ost_file_path))
    
    if (!existsSync(args.discord_token_file_path)) {
      throw Error(`couldn't find discord token`)
    }
    this.client.login(JSON.parse(readFileSync(args.discord_token_file_path)).discord_token)
    this.voice_conn = undefined
  }
	
  _get_channels = async () => {
		const guild_id = "414264829248012298"
		const guilds = await this.client.guilds.fetch()
    if (!guilds.cache.has(guild_id)) {
      throw `invalid guild id: ${guild_id}`
    }

    const channels = new Map()
    const guild = guilds.cache.get(guild_id)
    console.log(`Looking for voice channels in ${guild.name}`)
    guild.channels.cache.forEach((channel, id) => {
      if (channel.type === channel_type) {
        console.log(`  - ${channel.name}`)
        channels.set(channel.name, channel.id)
      }
    })

    return channels
  }
		
	_on_discord_ready = () => {
    console.log(`Logged in as ${this.client.user.tag}!`)
    console.log('This bot is part of the following guilds:')
    this.client.guilds.cache.forEach((guild, id) => {
      console.log(`  - ${guild.name} : ${id}`)
    })
  }

  _on_help = (msg, args) => {
    msg.reply(`
      Available Commands
      ------------------

      Play a song from url
        ?play --url <some url>
      
      Play a song from OST
        ?play --name <song name>
      
      Stop current song (if any)
        ?stop

      List all songs
        ?list
      
      List songs with given tags (enter 1 or more, comma separated)
        ?list --tags heles,ace,hype

      Detailed Song Info
        ?song_info --name <song name>

      List all tags being used
        ?tags
      
      Add a new song
        ?add_song --name <song name> --url <url> --tags heles,ace,hype  
      
      Remove a song
        ?remove_song --name <song name>

      Change song url
        ?edit_song --name <song name> --change_url <new url>

      Change song name
        ?edit_song --name <current name> --change_name <new name>

      Add tag to song
        ?edit_song --name <song name> --add_tag <new tag>

      Remove tag from song
        ?edit_song --name <song name> --remove_tag <tag to remove>

      Save the current OST to disk
        ?save_ost
      `
    )
  }

  _on_edit_add_tag = (msg, args) => {
    if (!args.add_tag.match("^[a-z_]*$")) {
      const err = `Tag name must be lowercase letters or dashes, got [${args.add_tag}]`
      console.log(err)
      msg.reply(err)
      return
    }

    if (this.ost[args.name].tags.includes(args.add_tag)) {
      const err = `[${args.name}] already has tag [${args.add_tag}]`
      console.log(err)
      msg.reply(err)
      return
    }

    this.ost[args.name].tags.push(args.add_tag)
    const ret = `[${args.add_tag}] added to [${args.name}]`
    console.log(ret)
    msg.reply(ret)
  }

  _on_edit_remove_tag = (msg, args) => {
    if (!this.ost[args.name].tags.includes(args.remove_tag)) {
      const err = `[${args.name}] never had tag [${args.remove_tag}]`
      console.log(err)
      msg.reply(err)
      return
    }

    this.ost[args.name].tags = this.ost[args.name].tags.filter(tag => {
      return tag != args.remove_tag
    })

    const ret = `[${args.remove_tag}] removed from [${args.name}]`
    console.log(ret)
    msg.reply(ret)
  }

  _on_edit_change_url = (msg, args) => {
    this.ost[args.name].url = args.change_url
    const ret = `[${args.name}] url changed to [${args.change_url}]`
    console.log(ret)
    msg.reply(ret)
  }

  _on_edit_change_name = (msg, args) => {
    if (!args.change_name.match("^[a-z0-9_]*$")) {
      const err = `Song name must be lowercase alphanumeric or dashes, got [${args.change_name}]`
      console.log(err)
      msg.reply(err)
      return
    }

    this.ost[args.change_name] = this.ost[args.name]
    delete this.ost[args.name]

    const ret = `[${args.name}] name changed to [${args.change_name}]`
    console.log(ret)
    msg.reply(ret)
  }

  _on_edit_song = (msg, args) => {
    if (args.name === undefined) {
      const err = "The name arg must be provided"
      console.log(err)
      msg.reply(err)
      return
    }

    if (this.ost[args.name] === undefined) {
      const err = `[${args.name}] not in the OST`
      console.log(err)
      msg.reply(err)
      return
    }

    if (args.add_tag !== undefined) {
      this._on_edit_add_tag(msg, args)
    }

    if (args.remove_tag !== undefined) {
      this._on_edit_remove_tag(msg, args)
    }

    if (args.change_url !== undefined) {
      this._on_edit_change_url(msg, args)
    }

    if (args.change_name !== undefined) {
      this._on_edit_change_name(msg, args)
    }
  }

  _on_add_song = (msg, args) => {
    if (args.name === undefined) {
      const err = "The name arg must be provided"
      console.log(err)
      msg.reply(err)
      return
    }

    if (args.url === undefined) {
      const err = "The url arg must be provided"
      console.log(err)
      msg.reply(err)
      return
    }

    if (this.ost[args.name] !== undefined) {
      const err = `[${args.name}] is already in the OST`
      console.log(err)
      msg.reply(err)
      return
    }

    if (!args.name.match("^[a-z0-9_]*$")) {
      const err = `Song name must be lowercase alphanumeric or dashes, got [${args.name}]`
      console.log(err)
      msg.reply(err)
      return
    }

    let tags = []
    if (args.tags !== undefined) {
      if (!args.name.match("^[a-z0-9_,]*$")) {
        const err = `Tag name list must be comma-separated, with only lowercase alphanumeric or dash characters, got [${args.tags}]`
        console.log(err)
        msg.reply(err)
        return
      }
      tags = args.tags.split(",")
    }

    this.ost[args.name] = {
      "tags": tags,
      "url": args.url  
    }

    const ret = `Song [${args.name} added to the OST]`
    console.log(ret)
    msg.reply(ret)
  }

  _on_remove_song = (msg, args) => {
    if (args.name === undefined) {
      const err = "The name arg must be provided"
      console.log(err)
      msg.reply(err)
      return
    }

    if (this.ost[args.name] === undefined) {
      const err = `[${args.name}] is not in the OST`
      console.log(err)
      msg.reply(err)
      return
    }

    delete this.ost[args.name]
    const ret = `[${args.name}] was deleted from the OST`
    console.log(ret)
    msg.reply(ret)
  }

  _on_save_ost = (msg, args) => {
    const ost_json = JSON.stringify(this.ost, null, 2)
    writeFileSync(this.ost_file_path, ost_json)
    const ret = `Saved the current ost list to disk`
    console.log(ret)
    msg.reply(ret)
  }

  _on_tags = (msg, args) => {
    const tags = Object.keys(this.ost).reduce((acc, key) => {
      this.ost[key].tags.forEach(elem => acc.add(elem))
      return acc
    }, new Set())

    const reply = Array.from(tags).join("\n")
    console.log(reply)
    msg.reply(`\n\nTags List\n------------\n${reply}`)
  }

  _on_song_info = (msg, args) => {
    if (args.name === undefined) {
      const err = "The name arg must be provided"
      console.log(err)
      msg.reply(err)
      return
    }

    if (this.ost[args.name] === undefined) {
      const err = `[${args.name}] is not in the OST`
      console.log(err)
      msg.reply(err)
      return
    }

    const ret = 
      `${args.name}
        Source
        --------
        [${this.ost[args.name].original_source}] - [${this.ost[args.name].original_name}]

        Tags
        ----
        [${this.ost[args.name].tags.join(", ")}]
        
        URL
        ---
        ${this.ost[args.name].url}`
    console.log(ret)
    msg.reply(ret)
  }

  _on_list = (msg, args) => {
    let filtered_ost = this.ost
    if (args.tags !== undefined) {
      const tags = args.tags.split(",")
      filtered_ost = Object.keys(this.ost).filter((key) => {
        return this.ost[key].tags.some(elem => {
          return Array.isArray(tags) ? tags.includes(elem) : tags == elem 
        })
      })
      .reduce((acc, key) => {
        acc[key] = this.ost[key]
        return acc
      }, {})
    }

    const reply = Object.keys(filtered_ost).map((key) => { 
      return `${key} - [${filtered_ost[key].tags.join(", ")}]`
    }).join("\n")

    console.log(reply)
    msg.reply(`\n\nSongs List\n------------\n${reply}`)
  }

  _on_play = (msg, args) => {
    let url = undefined
    if (args.url !== undefined) {
      url = args.url
    }	else if (args.name !== undefined) {
      if (this.ost[args.name] === undefined) {
        msg.reply(`Invalid song name: ${args.name}`)
        return
      }
      url = this.ost[args.name].url
    } else {
      msg.reply(`Either --url or --name must be specified, got neither`)
      return
    }
    
    msg.member.voice.channel.join().then(connection => {
      this.voice_conn = connection.play(ytdl(url))   
    }).catch(err => {
      console.log(err)
    })
  }
	
  _on_stop = (args) => {
    if (this.voice_conn !== undefined) {
      this.voice_conn.destroy()
      this.voice_conn = undefined
    }
  }

	_on_discord_message = async (msg) => {
    try {
      if (msg.author.bot) {
        return
      }

      const trimmed_msg = msg.content.trim()
      if (trimmed_msg[0] != _DISCORD_PREFIX) {
        return
      }
			
			const args = minimist(parseArgsStringToArgv(trimmed_msg.slice(1)), )
      console.log(`\nReceived msg from: [${msg.guild}: ${msg.channel.name}]`)
      switch (args["_"][0]) {
        case "play":
          this._on_play(msg, args)
          break
        case "stop":
          this._on_stop(args)
          break
        case "list":
          this._on_list(msg, args)
          break
        case "tags":
          this._on_tags(msg, args)
          break
        case "song_info":
          this._on_song_info(msg, args)
          break
        case "help":
          this._on_help(msg, args)
          break
        case "save_ost":
          this._on_save_ost(msg, args)
          break
        case "edit_song":
          this._on_edit_song(msg, args)
          break
        case "add_song":
          this._on_add_song(msg, args)
          break
        case "remove_song":
          this._on_remove_song(msg, args)
          break
        default:
          const err = `Command ${trimmed_msg} is invalid, try ?help for proper syntax`
          console.log(err)
          console.log(args)
          msg.reply(err)
      }
    } catch (e) {
      const err = `Caught exception while processing message: ${e}`
      console.log(err);
      msg.reply(err)
    }
  }
}

export {
    DiscordClient
}