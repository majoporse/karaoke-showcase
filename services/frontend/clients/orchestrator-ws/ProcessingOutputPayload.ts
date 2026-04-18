import ProcessingResult from "./ProcessingResult";
class ProcessingOutputPayload {
  private _currentStep: number;
  private _totalSteps?: number;
  private _desc: string;
  private _result?: ProcessingResult | null;
  private _additionalProperties?: Map<string, any>;

  constructor(input: {
    currentStep: number;
    totalSteps?: number;
    desc: string;
    result?: ProcessingResult | null;
    additionalProperties?: Map<string, any>;
  }) {
    this._currentStep = input.currentStep;
    this._totalSteps = input.totalSteps;
    this._desc = input.desc;
    this._result = input.result;
    this._additionalProperties = input.additionalProperties;
  }

  get currentStep(): number {
    return this._currentStep;
  }
  set currentStep(currentStep: number) {
    this._currentStep = currentStep;
  }

  get totalSteps(): number | undefined {
    return this._totalSteps;
  }
  set totalSteps(totalSteps: number | undefined) {
    this._totalSteps = totalSteps;
  }

  get desc(): string {
    return this._desc;
  }
  set desc(desc: string) {
    this._desc = desc;
  }

  get result(): ProcessingResult | null | undefined {
    return this._result;
  }
  set result(result: ProcessingResult | null | undefined) {
    this._result = result;
  }

  get additionalProperties(): Map<string, any> | undefined {
    return this._additionalProperties;
  }
  set additionalProperties(additionalProperties: Map<string, any> | undefined) {
    this._additionalProperties = additionalProperties;
  }

  public marshal(): string {
    let json = "{";
    if (this.currentStep !== undefined) {
      json += `"current_step": ${typeof this.currentStep === "number" || typeof this.currentStep === "boolean" ? this.currentStep : JSON.stringify(this.currentStep)},`;
    }
    if (this.totalSteps !== undefined) {
      json += `"total_steps": ${typeof this.totalSteps === "number" || typeof this.totalSteps === "boolean" ? this.totalSteps : JSON.stringify(this.totalSteps)},`;
    }
    if (this.desc !== undefined) {
      json += `"desc": ${typeof this.desc === "number" || typeof this.desc === "boolean" ? this.desc : JSON.stringify(this.desc)},`;
    }
    if (this.result !== undefined) {
      if (this.result instanceof ProcessingResult) {
        json += `"result": ${this.result.marshal()},`;
      } else {
        json += `"result": ${typeof this.result === "number" || typeof this.result === "boolean" ? this.result : JSON.stringify(this.result)},`;
      }
    }
    if (this.additionalProperties !== undefined) {
      for (const [key, value] of this.additionalProperties.entries()) {
        //Only unwrap those that are not already a property in the JSON object
        if (
          ["current_step", "total_steps", "desc", "result", "additionalProperties"].includes(
            String(key)
          )
        )
          continue;
        json += `"${key}": ${typeof value === "number" || typeof value === "boolean" ? value : JSON.stringify(value)},`;
      }
    }
    //Remove potential last comma
    return `${json.charAt(json.length - 1) === "," ? json.slice(0, json.length - 1) : json}}`;
  }

  public static unmarshal(json: string | object): ProcessingOutputPayload {
    const obj = typeof json === "object" ? json : JSON.parse(json);
    const instance = new ProcessingOutputPayload({} as any);

    if (obj["current_step"] !== undefined) {
      instance.currentStep = obj["current_step"];
    }
    if (obj["total_steps"] !== undefined) {
      instance.totalSteps = obj["total_steps"];
    }
    if (obj["desc"] !== undefined) {
      instance.desc = obj["desc"];
    }
    if (obj["result"] !== undefined) {
      instance.result = obj["result"];
    }

    instance.additionalProperties = new Map();
    const propsToCheck = Object.entries(obj).filter(([key]) => {
      return !["current_step", "total_steps", "desc", "result", "additionalProperties"].includes(
        key
      );
    });
    for (const [key, value] of propsToCheck) {
      instance.additionalProperties.set(key, value as any);
    }
    return instance;
  }
}
export default ProcessingOutputPayload;
