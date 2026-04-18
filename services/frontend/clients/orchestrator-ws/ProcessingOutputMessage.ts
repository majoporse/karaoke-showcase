import ProcessingOutputPayload from "./ProcessingOutputPayload";
class ProcessingOutputMessage {
  private _action?: "processing_output" = "processing_output";
  private _payload: ProcessingOutputPayload;
  private _additionalProperties?: Map<string, any>;

  constructor(input: {
    payload: ProcessingOutputPayload;
    additionalProperties?: Map<string, any>;
  }) {
    this._payload = input.payload;
    this._additionalProperties = input.additionalProperties;
  }

  get action(): "processing_output" | undefined {
    return this._action;
  }

  get payload(): ProcessingOutputPayload {
    return this._payload;
  }
  set payload(payload: ProcessingOutputPayload) {
    this._payload = payload;
  }

  get additionalProperties(): Map<string, any> | undefined {
    return this._additionalProperties;
  }
  set additionalProperties(additionalProperties: Map<string, any> | undefined) {
    this._additionalProperties = additionalProperties;
  }

  public marshal(): string {
    let json = "{";
    if (this.action !== undefined) {
      json += `"action": ${typeof this.action === "number" || typeof this.action === "boolean" ? this.action : JSON.stringify(this.action)},`;
    }
    if (this.payload !== undefined) {
      json += `"payload": ${this.payload.marshal()},`;
    }
    if (this.additionalProperties !== undefined) {
      for (const [key, value] of this.additionalProperties.entries()) {
        //Only unwrap those that are not already a property in the JSON object
        if (["action", "payload", "additionalProperties"].includes(String(key))) continue;
        json += `"${key}": ${typeof value === "number" || typeof value === "boolean" ? value : JSON.stringify(value)},`;
      }
    }
    //Remove potential last comma
    return `${json.charAt(json.length - 1) === "," ? json.slice(0, json.length - 1) : json}}`;
  }

  public static unmarshal(json: string | object): ProcessingOutputMessage {
    const obj = typeof json === "object" ? json : JSON.parse(json);
    const instance = new ProcessingOutputMessage({} as any);

    if (obj["payload"] !== undefined) {
      instance.payload = ProcessingOutputPayload.unmarshal(obj["payload"]);
    }

    instance.additionalProperties = new Map();
    const propsToCheck = Object.entries(obj).filter(([key]) => {
      return !["action", "payload", "additionalProperties"].includes(key);
    });
    for (const [key, value] of propsToCheck) {
      instance.additionalProperties.set(key, value as any);
    }
    return instance;
  }
}
export default ProcessingOutputMessage;
