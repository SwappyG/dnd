import { Constants, Client } from 'discord.js'
import { existsSync, readFileSync, writeFileSync } from 'fs'
import ytdl from 'ytdl-core'
import minimist from 'minimist';
import { parseArgsStringToArgv } from 'string-argv'


import { Mutex, Semaphore, withTimeout } from 'async-mutex'

const _DISCORD_PREFIX = "?"

const _STATE = {
  DISCONNECTED: 'DISCONNECTED',
  STOPPED: 'STOPPED',
  LOADING: 'LOADING',
  PLAYING: 'PLAYING'
}

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
    this.stream = undefined

    this.queue = []
    this.play_state = _STATE.DISCONNECTED
    this.now_playing = null

    this.mutex = new Mutex()

    this.loop = setInterval(() => {
      this.mutex.runExclusive(() => {
        switch (this.play_state) {
          case _STATE.DISCONNECTED:
            return
          case _STATE.STOPPED:
            const song = this.queue.shift()
            if (song === undefined) {
              return
            }

            this.play_state = _STATE.LOADING
            this.stream = this._play_ytdl(song.url, this.voice_conn)
            this.now_playing = song
            return
          case _STATE.LOADING:
            return
          case _STATE.PLAYING:
            return
        }
      })
    }, 10)

  }
		
	_on_discord_ready = () => {
    console.log(`Logged in as ${this.client.user.tag}!`)
    console.log('This bot is part of the following guilds:')
    this.client.guilds.cache.forEach((guild, id) => {
      console.log(`  - ${guild.name} : ${id}`)
    })
  }

  _on_help = (msg, args) => {
    msg.reply(
`\n
Available Commands
------------------

Attach bot to Voice Channel
  \`?connect\`

Play or Queue a song from url or from OST
  \`?play --url <some url>\`
  \`?play --name <song name>\`
  \`?queue --url <some url>\`
  \`?queue --name <some name>\`

Check current queue
  \`?queue --view\`

Skip current song or stop and delete entire queue
  \`?skip\`
  \`?stop\`

List songs and tags
  \`?tags\`
  \`?list\`
  \`?list --tags heles,ace,hype\`

Get information about a song or url
  \`?song_info --name <song name>\`
  \`?link_info --url <url>\`

Add or remove a song
  \`?remove_song --name <song name>\`
  \`?add_song --name <song name> --original_source <band,game,show> --original_name <orig song name> --url <url> --tags heles,ace\`  

Edit existing song
  \`?edit_song --name <song name> --change_url <new url>\`
  \`?edit_song --name <current name> --change_name <new name>\`
  \`?edit_song --name <song name> --add_tag <new tag>\`
  \`?edit_song --name <song name> --remove_tag <tag to remove>\`

Save the current OST to disk
  \`?save_ost\``
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

  _on_edit_change_original_name = (msg, args) => {
    this.ost[args.name].original_name = args.change_original_name
    const ret = `[${args.name}] original_name changed to [${args.change_original_name}]`
    console.log(ret)
    msg.reply(ret)
  }

  _on_edit_change_original_source = (msg, args) => {
    this.ost[args.name].original_source = args.change_original_source
    const ret = `[${args.name}] original_source changed to [${args.change_original_source}]`
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

    if (args.change_original_name !== undefined) {
      this._on_edit_change_original_name(msg, args)
    }

    if (args.change_original_source !== undefined) {
      this._on_edit_change_original_source(msg, args)
    }
  }

  _on_skip = () => {
    this.mutex.runExclusive(() => {
      if (this.stream !== undefined) {
        this.stream.end()
        this.stream = undefined
      }
    })
  }

  _on_queue = async (msg, args) => {
    if (args.view !== undefined) {
      this.mutex.runExclusive(() => {

        const make_row = (elem) => {
          if (elem.args.name !== undefined) {
            return `${elem.args.name} / (${this.ost[elem.args.name]?.original_name})\n`
          } else {
            return `${elem.info.videoDetails.title}\n`
          }
        }

        let ret = `\n\n`
        if (this.now_playing !== null) {
          ret = ret + `Now Playing:\n`
          ret = ret + `${make_row(this.now_playing)}`
        }

        ret = ret + `\nCurrent Queue:\n`
        ret = ret + this.queue.reduce((accum, elem, ii) => {
          return accum + make_row(elem)
        }, "")
        msg.reply(`${ret}`)
      })
      return
    }

    if (args.clear !== undefined) {
      this.mutex.runExclusive(() => {
        this.queue = []
        msg.reply(`Play queue cleared`)
      })
      return
    }

    const {url, info} = await this._parse_url_from_args(msg, args)
    if (url == null) {
      return
    }

    if (this.play_state === _STATE.DISCONNECTED) {
      this._on_connect(msg, args)  
    }

    this.mutex.runExclusive(() => {
      if (this.play_state === _STATE.DISCONNECTED) {
        return
      }
      console.log(this.queue)
      this.queue.push({'args': args, 'url': url, 'info': info})
      msg.reply(`Added song to queue`)
      console.log(this.queue)
    })
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

    if (args.original_source === undefined) {
      const err = "The original_source arg must be provided"
      console.log(err)
      msg.reply(err)
      return
    }

    if (args.original_name === undefined) {
      const err = "The original_name must be provided"
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
      if (!Array.isArray(tags)) {
        tags = [tags]
      }
    }

    this.ost[args.name] = {
      "original_source": args.original_source,
      "original_name": args.original_name,
      "tags": tags,
      "url": args.url  
    }

    const ret = `Song [${args.name}] from [${args.original_source}]: [${args.original_name}] added to the OST`
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
`\n
Song
----
[${args.name}]

Source
--------
[${this.ost[args.name].original_source}] - [${this.ost[args.name].original_name}]

Tags
----
[${this.ost[args.name].tags.join(", ")}]

URL
---
<${this.ost[args.name].url}>`
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

  _parse_url_from_args = async (msg, args) => {
    let url = undefined
    if (args.url !== undefined) {
      url = args.url
    }	else if (args.name !== undefined) {
      if (this.ost[args.name] === undefined) {
        msg.reply(`Invalid song name: ${args.name}`)
        return null
      }
      url = this.ost[args.name].url
    } else {
      msg.reply(`Either --url or --name must be specified, got neither`)
      return null
    }

    if (!ytdl.validateURL(url)) {
      const err = `the url <${url}> is invalid`
      console.log(err)
      msg.reply(err)
      return
    }

    const info = await this._get_url_info(url)

    return {'url': url, 'info': info} 
  }

  _get_url_info = (url) => {
    return ytdl.getBasicInfo(url)
  }

  _on_link_info = async (msg, args) => {
    const {url, info} = await this._parse_url_from_args(msg, args)
    if (url == null) {
      console.log("failed to parse url")
      return
    }

    console.log(info.videoDetails.title)

    const secs = info.videoDetails.lengthSeconds
    const ret =
      `\n\n` +
      `title: ${info.videoDetails.title}\n` +
      `length: ${parseInt(secs/60)}:${secs%60}\n` +
      `url: <${url}>\n`

    msg.reply(ret)
    console.log(ret)
  }

  _play_ytdl = (url, connection) => {
    const stream = connection.play(ytdl(url, { 
      'quality': 'highestaudio' 
    }))

    stream.on('start', () => {
      console.log(`started playing ${url}`)
      this.mutex.runExclusive(() => {
        this.play_state = _STATE.PLAYING
      })
    })

    stream.on('finish', () => {
      console.log(`finished playing ${url}`)
      this.mutex.runExclusive(() => {
        this.play_state = _STATE.STOPPED
      })
    })
    
    return stream
  }

  _on_connect = (msg, args, url) => {
    if (msg.member.voice.channel === null) {
      const err = `You must join a voice channel before connecting`
      console.log(err)
      msg.reply(err)
      return
    }

    this.mutex.runExclusive(() => {
      if (this.play_state !== _STATE.DISCONNECTED) {
        msg.reply('already connected')
        return
      }
    })

    msg.member.voice.channel.join().then((connection) => {
      this.mutex.runExclusive(() => {
        this.play_state = _STATE.STOPPED
        this.voice_conn = connection
        this.queue = []
        this.stream = null
        if (url !== undefined) {
          this.queue.push({'args': args, 'url': url})
        }
        msg.reply('successfully connected')
      })
    }).catch(err => {
      console.log("caught exception while trying to connect")
      console.log(err)
      this.mutex.runExclusive(() => {
        this.play_state = _STATE.DISCONNECTED
        this.play_state = _STATE.STOPPED
        this.voice_conn = connection
        this.queue = []
        this.stream = null
      })
    })
  }

  _on_play = async (msg, args) => {
    const {url, info} = await this._parse_url_from_args(msg, args)
    if (url === undefined) {
      return
    }

    if (this.play_state === _STATE.DISCONNECTED) {
      this._on_connect(msg, args, url)
      return
    }

    this.mutex.runExclusive(() => {
      if (this.play_state === _STATE.DISCONNECTED) {
        return
      }

      if (this.stream != null) {
        this.stream.end()
        this.stream = undefined
      }

      this.play_state = _STATE.STOPPED
      this.queue = []
      this.queue.push({'args': args, 'url': url, 'info': info})
    })
  }

  _on_stop = () => {
    this.mutex.runExclusive(() => {
      this.queue = []
    })
    this._on_skip()
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
		
			const args = minimist(parseArgsStringToArgv(trimmed_msg.slice(1)))
      console.log(`\nReceived msg from [${msg.member.displayName}] at [${msg.guild}: ${msg.channel.name}]`)
      console.log(args)
      switch (args["_"][0]) {
        case "connect":
          this._on_connect(msg, args)
          break;
        case "play":
          this._on_play(msg, args)
          break
        case "stop":
          this._on_stop()
          break
        case "queue":
          this._on_queue(msg, args)
          break
        case "skip":
          this._on_skip()
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
        case "link_info":
          this._on_link_info(msg, args)
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