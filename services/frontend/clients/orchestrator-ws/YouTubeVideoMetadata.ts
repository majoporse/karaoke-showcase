class YouTubeVideoMetadata {
  private _id: string;
  private _title: string;
  private _uploader: string;
  private _uploaderUrl: string;
  private _thumbnail: string;
  private _thumbnailUrl: string;
  private _description?: string | null;
  private _uploaderId?: string | null;
  private _duration?: number | null;
  private _viewCount?: number | null;
  private _likeCount?: number | null;
  private _dislikeCount?: number | null;
  private _uploadDate?: string | null;
  private _releaseDate?: string | null;
  private _categories?: string[] | null;
  private _tags?: string[] | null;
  private _ageLimit?: number | null;
  private _isLive?: boolean | null;
  private _channel?: string | null;
  private _channelId?: string | null;
  private _channelUrl?: string | null;
  private _durationString?: string | null;
  private _formatId?: string | null;
  private _formatNote?: string | null;
  private _width?: number | null;
  private _height?: number | null;
  private _resolution?: string | null;
  private _fps?: number | null;
  private _vcodec?: string | null;
  private _acodec?: string | null;
  private _extent?: string | null;
  private _format?: string | null;
  private _additionalProperties?: Map<string, any>;

  constructor(input: {
    id: string;
    title: string;
    uploader: string;
    uploaderUrl: string;
    thumbnail: string;
    thumbnailUrl: string;
    description?: string | null;
    uploaderId?: string | null;
    duration?: number | null;
    viewCount?: number | null;
    likeCount?: number | null;
    dislikeCount?: number | null;
    uploadDate?: string | null;
    releaseDate?: string | null;
    categories?: string[] | null;
    tags?: string[] | null;
    ageLimit?: number | null;
    isLive?: boolean | null;
    channel?: string | null;
    channelId?: string | null;
    channelUrl?: string | null;
    durationString?: string | null;
    formatId?: string | null;
    formatNote?: string | null;
    width?: number | null;
    height?: number | null;
    resolution?: string | null;
    fps?: number | null;
    vcodec?: string | null;
    acodec?: string | null;
    extent?: string | null;
    format?: string | null;
    additionalProperties?: Map<string, any>;
  }) {
    this._id = input.id;
    this._title = input.title;
    this._uploader = input.uploader;
    this._uploaderUrl = input.uploaderUrl;
    this._thumbnail = input.thumbnail;
    this._thumbnailUrl = input.thumbnailUrl;
    this._description = input.description;
    this._uploaderId = input.uploaderId;
    this._duration = input.duration;
    this._viewCount = input.viewCount;
    this._likeCount = input.likeCount;
    this._dislikeCount = input.dislikeCount;
    this._uploadDate = input.uploadDate;
    this._releaseDate = input.releaseDate;
    this._categories = input.categories;
    this._tags = input.tags;
    this._ageLimit = input.ageLimit;
    this._isLive = input.isLive;
    this._channel = input.channel;
    this._channelId = input.channelId;
    this._channelUrl = input.channelUrl;
    this._durationString = input.durationString;
    this._formatId = input.formatId;
    this._formatNote = input.formatNote;
    this._width = input.width;
    this._height = input.height;
    this._resolution = input.resolution;
    this._fps = input.fps;
    this._vcodec = input.vcodec;
    this._acodec = input.acodec;
    this._extent = input.extent;
    this._format = input.format;
    this._additionalProperties = input.additionalProperties;
  }

  get id(): string {
    return this._id;
  }
  set id(id: string) {
    this._id = id;
  }

  get title(): string {
    return this._title;
  }
  set title(title: string) {
    this._title = title;
  }

  get uploader(): string {
    return this._uploader;
  }
  set uploader(uploader: string) {
    this._uploader = uploader;
  }

  get uploaderUrl(): string {
    return this._uploaderUrl;
  }
  set uploaderUrl(uploaderUrl: string) {
    this._uploaderUrl = uploaderUrl;
  }

  get thumbnail(): string {
    return this._thumbnail;
  }
  set thumbnail(thumbnail: string) {
    this._thumbnail = thumbnail;
  }

  get thumbnailUrl(): string {
    return this._thumbnailUrl;
  }
  set thumbnailUrl(thumbnailUrl: string) {
    this._thumbnailUrl = thumbnailUrl;
  }

  get description(): string | null | undefined {
    return this._description;
  }
  set description(description: string | null | undefined) {
    this._description = description;
  }

  get uploaderId(): string | null | undefined {
    return this._uploaderId;
  }
  set uploaderId(uploaderId: string | null | undefined) {
    this._uploaderId = uploaderId;
  }

  get duration(): number | null | undefined {
    return this._duration;
  }
  set duration(duration: number | null | undefined) {
    this._duration = duration;
  }

  get viewCount(): number | null | undefined {
    return this._viewCount;
  }
  set viewCount(viewCount: number | null | undefined) {
    this._viewCount = viewCount;
  }

  get likeCount(): number | null | undefined {
    return this._likeCount;
  }
  set likeCount(likeCount: number | null | undefined) {
    this._likeCount = likeCount;
  }

  get dislikeCount(): number | null | undefined {
    return this._dislikeCount;
  }
  set dislikeCount(dislikeCount: number | null | undefined) {
    this._dislikeCount = dislikeCount;
  }

  get uploadDate(): string | null | undefined {
    return this._uploadDate;
  }
  set uploadDate(uploadDate: string | null | undefined) {
    this._uploadDate = uploadDate;
  }

  get releaseDate(): string | null | undefined {
    return this._releaseDate;
  }
  set releaseDate(releaseDate: string | null | undefined) {
    this._releaseDate = releaseDate;
  }

  get categories(): string[] | null | undefined {
    return this._categories;
  }
  set categories(categories: string[] | null | undefined) {
    this._categories = categories;
  }

  get tags(): string[] | null | undefined {
    return this._tags;
  }
  set tags(tags: string[] | null | undefined) {
    this._tags = tags;
  }

  get ageLimit(): number | null | undefined {
    return this._ageLimit;
  }
  set ageLimit(ageLimit: number | null | undefined) {
    this._ageLimit = ageLimit;
  }

  get isLive(): boolean | null | undefined {
    return this._isLive;
  }
  set isLive(isLive: boolean | null | undefined) {
    this._isLive = isLive;
  }

  get channel(): string | null | undefined {
    return this._channel;
  }
  set channel(channel: string | null | undefined) {
    this._channel = channel;
  }

  get channelId(): string | null | undefined {
    return this._channelId;
  }
  set channelId(channelId: string | null | undefined) {
    this._channelId = channelId;
  }

  get channelUrl(): string | null | undefined {
    return this._channelUrl;
  }
  set channelUrl(channelUrl: string | null | undefined) {
    this._channelUrl = channelUrl;
  }

  get durationString(): string | null | undefined {
    return this._durationString;
  }
  set durationString(durationString: string | null | undefined) {
    this._durationString = durationString;
  }

  get formatId(): string | null | undefined {
    return this._formatId;
  }
  set formatId(formatId: string | null | undefined) {
    this._formatId = formatId;
  }

  get formatNote(): string | null | undefined {
    return this._formatNote;
  }
  set formatNote(formatNote: string | null | undefined) {
    this._formatNote = formatNote;
  }

  get width(): number | null | undefined {
    return this._width;
  }
  set width(width: number | null | undefined) {
    this._width = width;
  }

  get height(): number | null | undefined {
    return this._height;
  }
  set height(height: number | null | undefined) {
    this._height = height;
  }

  get resolution(): string | null | undefined {
    return this._resolution;
  }
  set resolution(resolution: string | null | undefined) {
    this._resolution = resolution;
  }

  get fps(): number | null | undefined {
    return this._fps;
  }
  set fps(fps: number | null | undefined) {
    this._fps = fps;
  }

  get vcodec(): string | null | undefined {
    return this._vcodec;
  }
  set vcodec(vcodec: string | null | undefined) {
    this._vcodec = vcodec;
  }

  get acodec(): string | null | undefined {
    return this._acodec;
  }
  set acodec(acodec: string | null | undefined) {
    this._acodec = acodec;
  }

  get extent(): string | null | undefined {
    return this._extent;
  }
  set extent(extent: string | null | undefined) {
    this._extent = extent;
  }

  get format(): string | null | undefined {
    return this._format;
  }
  set format(format: string | null | undefined) {
    this._format = format;
  }

  get additionalProperties(): Map<string, any> | undefined {
    return this._additionalProperties;
  }
  set additionalProperties(additionalProperties: Map<string, any> | undefined) {
    this._additionalProperties = additionalProperties;
  }

  public marshal(): string {
    let json = "{";
    if (this.id !== undefined) {
      json += `"id": ${typeof this.id === "number" || typeof this.id === "boolean" ? this.id : JSON.stringify(this.id)},`;
    }
    if (this.title !== undefined) {
      json += `"title": ${typeof this.title === "number" || typeof this.title === "boolean" ? this.title : JSON.stringify(this.title)},`;
    }
    if (this.uploader !== undefined) {
      json += `"uploader": ${typeof this.uploader === "number" || typeof this.uploader === "boolean" ? this.uploader : JSON.stringify(this.uploader)},`;
    }
    if (this.uploaderUrl !== undefined) {
      json += `"uploader_url": ${typeof this.uploaderUrl === "number" || typeof this.uploaderUrl === "boolean" ? this.uploaderUrl : JSON.stringify(this.uploaderUrl)},`;
    }
    if (this.thumbnail !== undefined) {
      json += `"thumbnail": ${typeof this.thumbnail === "number" || typeof this.thumbnail === "boolean" ? this.thumbnail : JSON.stringify(this.thumbnail)},`;
    }
    if (this.thumbnailUrl !== undefined) {
      json += `"thumbnail_url": ${typeof this.thumbnailUrl === "number" || typeof this.thumbnailUrl === "boolean" ? this.thumbnailUrl : JSON.stringify(this.thumbnailUrl)},`;
    }
    if (this.description !== undefined) {
      json += `"description": ${typeof this.description === "number" || typeof this.description === "boolean" ? this.description : JSON.stringify(this.description)},`;
    }
    if (this.uploaderId !== undefined) {
      json += `"uploader_id": ${typeof this.uploaderId === "number" || typeof this.uploaderId === "boolean" ? this.uploaderId : JSON.stringify(this.uploaderId)},`;
    }
    if (this.duration !== undefined) {
      json += `"duration": ${typeof this.duration === "number" || typeof this.duration === "boolean" ? this.duration : JSON.stringify(this.duration)},`;
    }
    if (this.viewCount !== undefined) {
      json += `"view_count": ${typeof this.viewCount === "number" || typeof this.viewCount === "boolean" ? this.viewCount : JSON.stringify(this.viewCount)},`;
    }
    if (this.likeCount !== undefined) {
      json += `"like_count": ${typeof this.likeCount === "number" || typeof this.likeCount === "boolean" ? this.likeCount : JSON.stringify(this.likeCount)},`;
    }
    if (this.dislikeCount !== undefined) {
      json += `"dislike_count": ${typeof this.dislikeCount === "number" || typeof this.dislikeCount === "boolean" ? this.dislikeCount : JSON.stringify(this.dislikeCount)},`;
    }
    if (this.uploadDate !== undefined) {
      json += `"upload_date": ${typeof this.uploadDate === "number" || typeof this.uploadDate === "boolean" ? this.uploadDate : JSON.stringify(this.uploadDate)},`;
    }
    if (this.releaseDate !== undefined) {
      json += `"release_date": ${typeof this.releaseDate === "number" || typeof this.releaseDate === "boolean" ? this.releaseDate : JSON.stringify(this.releaseDate)},`;
    }
    if (this.categories !== undefined) {
      json += `"categories": ${typeof this.categories === "number" || typeof this.categories === "boolean" ? this.categories : JSON.stringify(this.categories)},`;
    }
    if (this.tags !== undefined) {
      json += `"tags": ${typeof this.tags === "number" || typeof this.tags === "boolean" ? this.tags : JSON.stringify(this.tags)},`;
    }
    if (this.ageLimit !== undefined) {
      json += `"age_limit": ${typeof this.ageLimit === "number" || typeof this.ageLimit === "boolean" ? this.ageLimit : JSON.stringify(this.ageLimit)},`;
    }
    if (this.isLive !== undefined) {
      json += `"is_live": ${typeof this.isLive === "number" || typeof this.isLive === "boolean" ? this.isLive : JSON.stringify(this.isLive)},`;
    }
    if (this.channel !== undefined) {
      json += `"channel": ${typeof this.channel === "number" || typeof this.channel === "boolean" ? this.channel : JSON.stringify(this.channel)},`;
    }
    if (this.channelId !== undefined) {
      json += `"channel_id": ${typeof this.channelId === "number" || typeof this.channelId === "boolean" ? this.channelId : JSON.stringify(this.channelId)},`;
    }
    if (this.channelUrl !== undefined) {
      json += `"channel_url": ${typeof this.channelUrl === "number" || typeof this.channelUrl === "boolean" ? this.channelUrl : JSON.stringify(this.channelUrl)},`;
    }
    if (this.durationString !== undefined) {
      json += `"duration_string": ${typeof this.durationString === "number" || typeof this.durationString === "boolean" ? this.durationString : JSON.stringify(this.durationString)},`;
    }
    if (this.formatId !== undefined) {
      json += `"format_id": ${typeof this.formatId === "number" || typeof this.formatId === "boolean" ? this.formatId : JSON.stringify(this.formatId)},`;
    }
    if (this.formatNote !== undefined) {
      json += `"format_note": ${typeof this.formatNote === "number" || typeof this.formatNote === "boolean" ? this.formatNote : JSON.stringify(this.formatNote)},`;
    }
    if (this.width !== undefined) {
      json += `"width": ${typeof this.width === "number" || typeof this.width === "boolean" ? this.width : JSON.stringify(this.width)},`;
    }
    if (this.height !== undefined) {
      json += `"height": ${typeof this.height === "number" || typeof this.height === "boolean" ? this.height : JSON.stringify(this.height)},`;
    }
    if (this.resolution !== undefined) {
      json += `"resolution": ${typeof this.resolution === "number" || typeof this.resolution === "boolean" ? this.resolution : JSON.stringify(this.resolution)},`;
    }
    if (this.fps !== undefined) {
      json += `"fps": ${typeof this.fps === "number" || typeof this.fps === "boolean" ? this.fps : JSON.stringify(this.fps)},`;
    }
    if (this.vcodec !== undefined) {
      json += `"vcodec": ${typeof this.vcodec === "number" || typeof this.vcodec === "boolean" ? this.vcodec : JSON.stringify(this.vcodec)},`;
    }
    if (this.acodec !== undefined) {
      json += `"acodec": ${typeof this.acodec === "number" || typeof this.acodec === "boolean" ? this.acodec : JSON.stringify(this.acodec)},`;
    }
    if (this.extent !== undefined) {
      json += `"extent": ${typeof this.extent === "number" || typeof this.extent === "boolean" ? this.extent : JSON.stringify(this.extent)},`;
    }
    if (this.format !== undefined) {
      json += `"format": ${typeof this.format === "number" || typeof this.format === "boolean" ? this.format : JSON.stringify(this.format)},`;
    }
    if (this.additionalProperties !== undefined) {
      for (const [key, value] of this.additionalProperties.entries()) {
        //Only unwrap those that are not already a property in the JSON object
        if (
          [
            "id",
            "title",
            "uploader",
            "uploader_url",
            "thumbnail",
            "thumbnail_url",
            "description",
            "uploader_id",
            "duration",
            "view_count",
            "like_count",
            "dislike_count",
            "upload_date",
            "release_date",
            "categories",
            "tags",
            "age_limit",
            "is_live",
            "channel",
            "channel_id",
            "channel_url",
            "duration_string",
            "format_id",
            "format_note",
            "width",
            "height",
            "resolution",
            "fps",
            "vcodec",
            "acodec",
            "extent",
            "format",
            "additionalProperties",
          ].includes(String(key))
        )
          continue;
        json += `"${key}": ${typeof value === "number" || typeof value === "boolean" ? value : JSON.stringify(value)},`;
      }
    }
    //Remove potential last comma
    return `${json.charAt(json.length - 1) === "," ? json.slice(0, json.length - 1) : json}}`;
  }

  public static unmarshal(json: string | object): YouTubeVideoMetadata {
    const obj = typeof json === "object" ? json : JSON.parse(json);
    const instance = new YouTubeVideoMetadata({} as any);

    if (obj["id"] !== undefined) {
      instance.id = obj["id"];
    }
    if (obj["title"] !== undefined) {
      instance.title = obj["title"];
    }
    if (obj["uploader"] !== undefined) {
      instance.uploader = obj["uploader"];
    }
    if (obj["uploader_url"] !== undefined) {
      instance.uploaderUrl = obj["uploader_url"];
    }
    if (obj["thumbnail"] !== undefined) {
      instance.thumbnail = obj["thumbnail"];
    }
    if (obj["thumbnail_url"] !== undefined) {
      instance.thumbnailUrl = obj["thumbnail_url"];
    }
    if (obj["description"] !== undefined) {
      instance.description = obj["description"];
    }
    if (obj["uploader_id"] !== undefined) {
      instance.uploaderId = obj["uploader_id"];
    }
    if (obj["duration"] !== undefined) {
      instance.duration = obj["duration"];
    }
    if (obj["view_count"] !== undefined) {
      instance.viewCount = obj["view_count"];
    }
    if (obj["like_count"] !== undefined) {
      instance.likeCount = obj["like_count"];
    }
    if (obj["dislike_count"] !== undefined) {
      instance.dislikeCount = obj["dislike_count"];
    }
    if (obj["upload_date"] !== undefined) {
      instance.uploadDate = obj["upload_date"];
    }
    if (obj["release_date"] !== undefined) {
      instance.releaseDate = obj["release_date"];
    }
    if (obj["categories"] !== undefined) {
      instance.categories = obj["categories"];
    }
    if (obj["tags"] !== undefined) {
      instance.tags = obj["tags"];
    }
    if (obj["age_limit"] !== undefined) {
      instance.ageLimit = obj["age_limit"];
    }
    if (obj["is_live"] !== undefined) {
      instance.isLive = obj["is_live"];
    }
    if (obj["channel"] !== undefined) {
      instance.channel = obj["channel"];
    }
    if (obj["channel_id"] !== undefined) {
      instance.channelId = obj["channel_id"];
    }
    if (obj["channel_url"] !== undefined) {
      instance.channelUrl = obj["channel_url"];
    }
    if (obj["duration_string"] !== undefined) {
      instance.durationString = obj["duration_string"];
    }
    if (obj["format_id"] !== undefined) {
      instance.formatId = obj["format_id"];
    }
    if (obj["format_note"] !== undefined) {
      instance.formatNote = obj["format_note"];
    }
    if (obj["width"] !== undefined) {
      instance.width = obj["width"];
    }
    if (obj["height"] !== undefined) {
      instance.height = obj["height"];
    }
    if (obj["resolution"] !== undefined) {
      instance.resolution = obj["resolution"];
    }
    if (obj["fps"] !== undefined) {
      instance.fps = obj["fps"];
    }
    if (obj["vcodec"] !== undefined) {
      instance.vcodec = obj["vcodec"];
    }
    if (obj["acodec"] !== undefined) {
      instance.acodec = obj["acodec"];
    }
    if (obj["extent"] !== undefined) {
      instance.extent = obj["extent"];
    }
    if (obj["format"] !== undefined) {
      instance.format = obj["format"];
    }

    instance.additionalProperties = new Map();
    const propsToCheck = Object.entries(obj).filter(([key]) => {
      return ![
        "id",
        "title",
        "uploader",
        "uploader_url",
        "thumbnail",
        "thumbnail_url",
        "description",
        "uploader_id",
        "duration",
        "view_count",
        "like_count",
        "dislike_count",
        "upload_date",
        "release_date",
        "categories",
        "tags",
        "age_limit",
        "is_live",
        "channel",
        "channel_id",
        "channel_url",
        "duration_string",
        "format_id",
        "format_note",
        "width",
        "height",
        "resolution",
        "fps",
        "vcodec",
        "acodec",
        "extent",
        "format",
        "additionalProperties",
      ].includes(key);
    });
    for (const [key, value] of propsToCheck) {
      instance.additionalProperties.set(key, value as any);
    }
    return instance;
  }
}
export default YouTubeVideoMetadata;
