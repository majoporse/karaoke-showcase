import Chunk from "./Chunk";
import YouTubeVideoMetadata from "./YouTubeVideoMetadata";
class ProcessingResult {
  private _success?: boolean | null;
  private _vocalsPath?: string | null;
  private _accompanimentPath?: string | null;
  private _lyrics?: string | null;
  private _chunks?: Chunk[] | null;
  private _ytMetadata?: YouTubeVideoMetadata | null;
  private _error?: string | null;
  private _additionalProperties?: Map<string, any>;

  constructor(input: {
    success?: boolean | null;
    vocalsPath?: string | null;
    accompanimentPath?: string | null;
    lyrics?: string | null;
    chunks?: Chunk[] | null;
    ytMetadata?: YouTubeVideoMetadata | null;
    error?: string | null;
    additionalProperties?: Map<string, any>;
  }) {
    this._success = input.success;
    this._vocalsPath = input.vocalsPath;
    this._accompanimentPath = input.accompanimentPath;
    this._lyrics = input.lyrics;
    this._chunks = input.chunks;
    this._ytMetadata = input.ytMetadata;
    this._error = input.error;
    this._additionalProperties = input.additionalProperties;
  }

  get success(): boolean | null | undefined {
    return this._success;
  }
  set success(success: boolean | null | undefined) {
    this._success = success;
  }

  get vocalsPath(): string | null | undefined {
    return this._vocalsPath;
  }
  set vocalsPath(vocalsPath: string | null | undefined) {
    this._vocalsPath = vocalsPath;
  }

  get accompanimentPath(): string | null | undefined {
    return this._accompanimentPath;
  }
  set accompanimentPath(accompanimentPath: string | null | undefined) {
    this._accompanimentPath = accompanimentPath;
  }

  get lyrics(): string | null | undefined {
    return this._lyrics;
  }
  set lyrics(lyrics: string | null | undefined) {
    this._lyrics = lyrics;
  }

  get chunks(): Chunk[] | null | undefined {
    return this._chunks;
  }
  set chunks(chunks: Chunk[] | null | undefined) {
    this._chunks = chunks;
  }

  get ytMetadata(): YouTubeVideoMetadata | null | undefined {
    return this._ytMetadata;
  }
  set ytMetadata(ytMetadata: YouTubeVideoMetadata | null | undefined) {
    this._ytMetadata = ytMetadata;
  }

  get error(): string | null | undefined {
    return this._error;
  }
  set error(error: string | null | undefined) {
    this._error = error;
  }

  get additionalProperties(): Map<string, any> | undefined {
    return this._additionalProperties;
  }
  set additionalProperties(additionalProperties: Map<string, any> | undefined) {
    this._additionalProperties = additionalProperties;
  }

  public marshal(): string {
    let json = "{";
    if (this.success !== undefined) {
      json += `"success": ${typeof this.success === "number" || typeof this.success === "boolean" ? this.success : JSON.stringify(this.success)},`;
    }
    if (this.vocalsPath !== undefined) {
      json += `"vocals_path": ${typeof this.vocalsPath === "number" || typeof this.vocalsPath === "boolean" ? this.vocalsPath : JSON.stringify(this.vocalsPath)},`;
    }
    if (this.accompanimentPath !== undefined) {
      json += `"accompaniment_path": ${typeof this.accompanimentPath === "number" || typeof this.accompanimentPath === "boolean" ? this.accompanimentPath : JSON.stringify(this.accompanimentPath)},`;
    }
    if (this.lyrics !== undefined) {
      json += `"lyrics": ${typeof this.lyrics === "number" || typeof this.lyrics === "boolean" ? this.lyrics : JSON.stringify(this.lyrics)},`;
    }
    if (this.chunks !== undefined) {
      json += `"chunks": ${typeof this.chunks === "number" || typeof this.chunks === "boolean" ? this.chunks : JSON.stringify(this.chunks)},`;
    }
    if (this.ytMetadata !== undefined) {
      if (this.ytMetadata instanceof YouTubeVideoMetadata) {
        json += `"yt_metadata": ${this.ytMetadata.marshal()},`;
      } else {
        json += `"yt_metadata": ${typeof this.ytMetadata === "number" || typeof this.ytMetadata === "boolean" ? this.ytMetadata : JSON.stringify(this.ytMetadata)},`;
      }
    }
    if (this.error !== undefined) {
      json += `"error": ${typeof this.error === "number" || typeof this.error === "boolean" ? this.error : JSON.stringify(this.error)},`;
    }
    if (this.additionalProperties !== undefined) {
      for (const [key, value] of this.additionalProperties.entries()) {
        //Only unwrap those that are not already a property in the JSON object
        if (
          [
            "success",
            "vocals_path",
            "accompaniment_path",
            "lyrics",
            "chunks",
            "yt_metadata",
            "error",
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

  public static unmarshal(json: string | object): ProcessingResult {
    const obj = typeof json === "object" ? json : JSON.parse(json);
    const instance = new ProcessingResult({} as any);

    if (obj["success"] !== undefined) {
      instance.success = obj["success"];
    }
    if (obj["vocals_path"] !== undefined) {
      instance.vocalsPath = obj["vocals_path"];
    }
    if (obj["accompaniment_path"] !== undefined) {
      instance.accompanimentPath = obj["accompaniment_path"];
    }
    if (obj["lyrics"] !== undefined) {
      instance.lyrics = obj["lyrics"];
    }
    if (obj["chunks"] !== undefined) {
      instance.chunks = obj["chunks"];
    }
    if (obj["yt_metadata"] !== undefined) {
      instance.ytMetadata = obj["yt_metadata"];
    }
    if (obj["error"] !== undefined) {
      instance.error = obj["error"];
    }

    instance.additionalProperties = new Map();
    const propsToCheck = Object.entries(obj).filter(([key]) => {
      return ![
        "success",
        "vocals_path",
        "accompaniment_path",
        "lyrics",
        "chunks",
        "yt_metadata",
        "error",
        "additionalProperties",
      ].includes(key);
    });
    for (const [key, value] of propsToCheck) {
      instance.additionalProperties.set(key, value as any);
    }
    return instance;
  }
}
export default ProcessingResult;
