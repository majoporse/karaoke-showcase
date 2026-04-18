class Chunk {
  private _start: number;
  private _end: number;
  private _reservedText: string;
  private _additionalProperties?: Map<string, any>;

  constructor(input: {
    start: number;
    end: number;
    reservedText: string;
    additionalProperties?: Map<string, any>;
  }) {
    this._start = input.start;
    this._end = input.end;
    this._reservedText = input.reservedText;
    this._additionalProperties = input.additionalProperties;
  }

  get start(): number {
    return this._start;
  }
  set start(start: number) {
    this._start = start;
  }

  get end(): number {
    return this._end;
  }
  set end(end: number) {
    this._end = end;
  }

  get reservedText(): string {
    return this._reservedText;
  }
  set reservedText(reservedText: string) {
    this._reservedText = reservedText;
  }

  get additionalProperties(): Map<string, any> | undefined {
    return this._additionalProperties;
  }
  set additionalProperties(additionalProperties: Map<string, any> | undefined) {
    this._additionalProperties = additionalProperties;
  }

  public marshal(): string {
    let json = "{";
    if (this.start !== undefined) {
      json += `"start": ${typeof this.start === "number" || typeof this.start === "boolean" ? this.start : JSON.stringify(this.start)},`;
    }
    if (this.end !== undefined) {
      json += `"end": ${typeof this.end === "number" || typeof this.end === "boolean" ? this.end : JSON.stringify(this.end)},`;
    }
    if (this.reservedText !== undefined) {
      json += `"text": ${typeof this.reservedText === "number" || typeof this.reservedText === "boolean" ? this.reservedText : JSON.stringify(this.reservedText)},`;
    }
    if (this.additionalProperties !== undefined) {
      for (const [key, value] of this.additionalProperties.entries()) {
        //Only unwrap those that are not already a property in the JSON object
        if (["start", "end", "text", "additionalProperties"].includes(String(key))) continue;
        json += `"${key}": ${typeof value === "number" || typeof value === "boolean" ? value : JSON.stringify(value)},`;
      }
    }
    //Remove potential last comma
    return `${json.charAt(json.length - 1) === "," ? json.slice(0, json.length - 1) : json}}`;
  }

  public static unmarshal(json: string | object): Chunk {
    const obj = typeof json === "object" ? json : JSON.parse(json);
    const instance = new Chunk({} as any);

    if (obj["start"] !== undefined) {
      instance.start = obj["start"];
    }
    if (obj["end"] !== undefined) {
      instance.end = obj["end"];
    }
    if (obj["text"] !== undefined) {
      instance.reservedText = obj["text"];
    }

    instance.additionalProperties = new Map();
    const propsToCheck = Object.entries(obj).filter(([key]) => {
      return !["start", "end", "text", "additionalProperties"].includes(key);
    });
    for (const [key, value] of propsToCheck) {
      instance.additionalProperties.set(key, value as any);
    }
    return instance;
  }
}
export default Chunk;
