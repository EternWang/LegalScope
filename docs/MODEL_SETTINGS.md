# Model settings

Provider references checked on **9 October 2026**. This guide covers all 28 model groups. The [JSON catalog](../evaluation/provider_defaults.json) records values, API scope and official sources; the [OpenRouter snapshot](../evaluation/openrouter_defaults_snapshot.json) preserves the model metadata returned on that date.

These are current provider defaults, not a reconstruction of historical requests. The [recorded generation configurations](../evaluation/generation_configs.json) retain the explicit parameters recovered from the August runs, including temperature 0 where set. Default values do not replace those settings or alter the released scores.

## OpenAI

The general Responses API schema assigns 1 to `temperature` and `top_p`. These schema defaults do not establish support for changing sampling parameters in every model or reasoning mode. Leave sampling parameters omitted unless the selected model supports them. API defaults also do not determine a Codex client configuration.

| Model group | Temperature, generic schema | Top-p, generic schema | Model reasoning default | Paper variant | Sources |
| --- | ---: | ---: | --- | --- | --- |
| GPT-5.4 Mini | 1 | 1 | none | Unspecified | [Schema](https://github.com/openai/openai-openapi/blob/main/openapi.json); [model](https://developers.openai.com/api/docs/models/gpt-5.4-mini) |
| GPT-5.5 Medium | 1 | 1 | medium | medium | [Schema](https://github.com/openai/openai-openapi/blob/main/openapi.json); [model](https://developers.openai.com/api/docs/models/gpt-5.5) |
| GPT-5.5 High | 1 | 1 | medium | high | [Schema](https://github.com/openai/openai-openapi/blob/main/openapi.json); [model](https://developers.openai.com/api/docs/models/gpt-5.5) |

The checked schema gives no numeric default for `max_output_tokens`. The model pages list a 128,000-token output ceiling; that ceiling is not recorded here as a default request budget. GPT-5.5 High retains its explicit high variant even though the model default is medium.

## Google Gemini

Google Cloud publishes the numeric sampling values below. For the Gemini Developer API, the reference delegates sampling defaults to `getModel`; these Cloud values are kept as a separately scoped reference. The Developer API defines an omitted `maxOutputTokens` through the model output limit, which the three model pages list as 65,536.

| Model group | Cloud temperature | Cloud top-p | Cloud top-k, fixed | Thinking default | Paper variant | Sources |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Gemini 2.5 Flash | 1 | 0.95 | 64 | dynamic (thinkingBudget=-1) | Unspecified | [Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash); [model](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash) |
| Gemini 3 Flash | 1 | 0.95 | 64 | high | Unspecified | [Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-flash); [model](https://ai.google.dev/gemini-api/docs/models/gemini-3-flash-preview) |
| Gemini 3 Flash Low | 1 | 0.95 | 64 | high | low | [Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-flash); [model](https://ai.google.dev/gemini-api/docs/models/gemini-3-flash-preview) |
| Gemini-3.5-Flash | 1 | 0.95 | 64 | medium | Unspecified | [Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash); [model](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash) |

[Thinking modes](https://ai.google.dev/gemini-api/docs/generate-content/thinking) documents dynamic thinking for 2.5 Flash, high for 3 Flash and medium for 3.5 Flash. The Low experiment remains a distinct variant. [GenerationConfig](https://ai.google.dev/api/generate-content#v1beta.GenerationConfig) gives `candidateCount=1` and a randomly generated seed when omitted.

## OpenRouter

The table transcribes `default_parameters` from the [model catalog](https://openrouter.ai/api/v1/models). **Not published** means that the field was null or absent; it does not mean 0 or 1. Under the [parameter contract](https://openrouter.ai/docs/api_reference/parameters), omitted sampling parameters are left to the upstream provider. A catalog value is not proof of the value used on a past routed request.

| Model group | OpenRouter model ID | Temperature | Top-p | Top-k |
| --- | --- | ---: | ---: | ---: |
| Grok 4.20 | `x-ai/grok-4.20` | Not published | Not published | Not published |
| DeepSeek R1 | `deepseek/deepseek-r1` | Not published | Not published | Not published |
| Qwen3 Max | `qwen/qwen3-max` | 1 | 1 | Not published |
| Deep Cogito 671B | `deepcogito/cogito-v2.1-671b` | Not published | Not published | Not published |
| Qwen3 Max Thinking | `qwen/qwen3-max-thinking` | Not published | Not published | Not published |
| GLM-5 low | `z-ai/glm-5` | 1 | 0.95 | Not published |
| Qwen3 235B A22B | `qwen/qwen3-235b-a22b-2507` | Not published | Not published | Not published |
| DeepSeek V3.2 | `deepseek/deepseek-v3.2` | 1 | 0.95 | Not published |
| Kimi K2 Thinking | `moonshotai/kimi-k2-thinking` | Not published | Not published | Not published |
| Grok 4.3 | `x-ai/grok-4.3` | Not published | Not published | Not published |
| Grok 4.5 | `x-ai/grok-4.5` | Not published | Not published | Not published |
| Command A | `cohere/command-a` | Not published | Not published | Not published |
| LLaMA 3.1 8B Instruct | `meta-llama/llama-3.1-8b-instruct` | Not published | Not published | Not published |
| Command R+ | `cohere/command-r-plus-08-2024` | Not published | Not published | Not published |
| Qwen3.5-9B | `qwen/qwen3.5-9b` | Not published | Not published | Not published |
| Qwen3.8-27B | `qwen/qwen3.8-27b` | 1 | 0.95 | 20 |
| Qwen3.8-2.4T-A95B | `qwen/qwen3.8-2.4t-a95b` | 1 | 0.95 | 20 |
| GLM-5.3 | `z-ai/glm-5.3` | 1 | 0.95 | Not published |
| Kimi-K3 | `moonshotai/kimi-k3` | Not published | 0.95 | Not published |
| DeepSeek-V4-Pro | `deepseek/deepseek-v4-pro` | 1 | 1 | Not published |
| DeepSeek-V4-Flash | `deepseek/deepseek-v4-flash` | Not published | Not published | Not published |

The Deep Cogito alias was not present in the current catalog. The other aliases were present. No uniform numeric output budget, reasoning effort or seed is supplied for these groups by this catalog. `top_provider.max_completion_tokens` in the snapshot is a provider ceiling, not a default request budget.

## Native provider and model release references

These additional checks apply to the named native API or local model release. They are not substituted for an unknown OpenRouter route. Recommendations are labelled separately from defaults.

| Model or family | Scope | Published values | Source |
| --- | --- | --- | --- |
| Grok 4.20, 4.3, 4.5 | xAI native Chat Completions | Output budget defaults to 128,000 visible tokens. Sampling defaults not specified. 4.3 reasoning defaults to low; 4.5 to high. | [API](https://docs.x.ai/developers/rest-api-reference/inference/chat-completions); [4.3](https://docs.x.ai/developers/models/grok-4.3); [4.5](https://docs.x.ai/developers/models/grok-4.5) |
| DeepSeek R1 | Author generation configuration | Temperature 0.6; top-p 0.95 | [Configuration](https://huggingface.co/deepseek-ai/DeepSeek-R1/blob/main/generation_config.json) |
| DeepSeek V3.2 | Author generation configuration | Temperature 1; top-p 0.95 | [Configuration](https://huggingface.co/deepseek-ai/DeepSeek-V3.2/blob/main/generation_config.json) |
| Qwen3 235B A22B | Author Instruct-2507 configuration | Temperature 0.7; top-p 0.8; top-k 20 | [Configuration](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507/blob/main/generation_config.json) |
| Qwen3.5-9B | Alibaba Model Studio, family defaults | Non-thinking: temperature 0.7, top-p 0.8. Thinking: temperature 0.6, top-p 0.95. Top-k 20. | [API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions) |
| Qwen3.8-27B; Qwen3.8-2.4T-A95B | Author generation configurations | Temperature 1; top-p 0.95; top-k 20 | [27B](https://huggingface.co/Qwen/Qwen3.8-27B/blob/main/generation_config.json); [2.4T](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/blob/main/generation_config.json) |
| GLM-5; GLM-5.3 | Z.AI native API | Temperature 1; top-p 0.95. GLM-5.3 reasoning defaults to max. No numeric default output budget stated. | [API](https://docs.z.ai/api-reference/llm/chat-completion) |
| Command A; Command R+ | Cohere native v2 API | Temperature 0.3; p 0.75; k 0; frequency and presence penalties 0. Output defaults to the model limit, labelled 8k and 4k respectively. | [API](https://docs.cohere.com/reference/chat); [models](https://docs.cohere.com/docs/models) |
| Kimi K3 | Kimi native API | Fixed temperature 1, top-p 0.95, n 1, penalties 0. Output budget 131,072; reasoning max. Thinking is always enabled. | [Model](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart); [parameters](https://platform.kimi.ai/docs/api/models-overview) |
| Kimi K2 Thinking | Author recommendation | Recommended temperature 1; not a verified omitted-parameter API default. | [Model card](https://huggingface.co/moonshotai/Kimi-K2-Thinking) |
| DeepSeek V4 Pro; V4 Flash | DeepSeek native API | Temperature 1; top-p 1. Output defaults: 8,192 non-thinking, 65,536 thinking, 131,072 at max effort. Default effort high. | [API](https://api-docs.deepseek.com/api/create-chat-completion/) |
| Deep Cogito 671B; LLaMA 3.1 8B Instruct | Model release / hosted route | No verified numeric API defaults in the checked references. Example settings are not treated as defaults. | [Cogito](https://huggingface.co/deepcogito/cogito-671b-v2.1); [Llama](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) |

For the native DeepSeek V4 API, temperature does not affect thinking mode. Top-p is fixed at 1 outside thinking mode; in thinking mode values below 0.95 are treated as 0.95. Kimi K3 native API sampling values are fixed and should be omitted from requests. These constraints must be checked when moving between a native API and OpenRouter.

## Using the records

Use the recorded configuration when reproducing a documented run. For a new run, record the actual endpoint, model ID, explicit parameters, omitted parameters, provider route and date. A provider default can change without the paper model label changing. Preserve the Medium, High and Low variants when comparing results.

In the JSON catalog, null means no verified value in that source and scope. Native defaults, author configuration files and recommendations have distinct `kind` labels. The catalog is reference data; it is not loaded automatically by the generation runner.
