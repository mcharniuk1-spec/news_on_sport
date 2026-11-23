# fal — повні вхідні параметри 30 відібраних endpoints

Знімок живих compact-схем, 19 листопада 2026. Кожен рядок відповідає одному полю; обмеження в описі також мають значення. Вкладені об’єкти, масиви, regex та оригінальні контракти є у [галузевих JSONL](catalog/). Повний каталог інших моделей — [CSV](catalog/fal-endpoints.csv).

## Генерація відео

### bytedance/seedance-2.5/flash/text-to-video

[Сторінка моделі](https://fal.ai/models/bytedance/seedance-2.5/flash/text-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `generate_audio` | опційне | boolean | true | Whether to generate synchronized audio for the video, including sound effects, ambient sounds, and lip-synced speech. The cost of video generation is the same regardless of whether audio is generated or not. |
| `resolution` | опційне | 480p \| 720p | "720p" | Video resolution - 480p for faster generation, 720p for quality. |
| `aspect_ratio` | опційне | auto \| 21:9 \| 16:9 \| 4:3 \| 1:1 \| 3:4 \| 9:16 | "auto" | The aspect ratio of the generated video. Use 16:9 for landscape, 9:16 for portrait/vertical, 1:1 for square, 21:9 for ultrawide cinematic, or auto to let the model decide. |
| `prompt` | обов’язкове | string | — | The text prompt used to generate the video |
| `codec` | опційне | auto \| H264 \| H265 | "auto" | 'auto' retains default video codec behaviour; 'H264' uses H.264; 'H265' uses H.265. |
| `bitrate_mode` | опційне | standard \| high | "standard" | Output bitrate mode. 'high' requests a higher-quality, larger-file encode from the model; 'standard' uses the default bitrate. |
| `duration` | опційне | auto \| 4 \| 5 \| 6 \| 7 \| 8 \| 9 \| 10 \| 11 \| 12 \| 13 \| 14 \| 15 \| 16 \| 17 \| 18 \| 19 \| 20 \| 21 \| 22 \| 23 \| 24 \| 25 \| 26 \| 27 \| 28 \| 29 \| 30 | "auto" | Duration of the video in seconds. Supports 4 to 30 seconds, or auto to let the model decide based on the prompt. |
| `end_user_id` | опційне | string / null | — | The unique user ID of the end user. |

Вихідні поля: `draft_id`, `seed`, `video`.

### bytedance/seedance-2.5/us/reference-to-video

[Сторінка моделі](https://fal.ai/models/bytedance/seedance-2.5/us/reference-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `duration` | опційне | auto \| 4 \| 5 \| 6 \| 7 \| 8 \| 9 \| 10 \| 11 \| 12 \| 13 \| 14 \| 15 \| 16 \| 17 \| 18 \| 19 \| 20 \| 21 \| 22 \| 23 \| 24 \| 25 \| 26 \| 27 \| 28 \| 29 \| 30 | "auto" | Duration of the video in seconds. Supports 4 to 30 seconds, or auto to let the model decide based on the prompt. |
| `end_user_id` | опційне | string / null | — | The unique user ID of the end user. |
| `generate_audio` | опційне | boolean | true | Whether to generate synchronized audio for the video, including sound effects, ambient sounds, and lip-synced speech. The cost of video generation is the same regardless of whether audio is generated or not. |
| `video_urls` | опційне | array[string] | — | Reference videos to guide video generation. Refer to them in the prompt as @Video1, @Video2, etc. Supported formats: MP4, MOV. Up to 10 videos. Each video must be 1.8 to 30.2 seconds and no larger than 200 MB; combined duration must not exceed 30.2 seconds. Dimensions must be 300 to 6,000 pixels per side, aspect ratio 0.4 to 2.5, and frame rate 24 to 60 FPS. |
| `resolution` | опційне | 480p \| 720p \| 1080p \| 4k | "720p" | Video resolution - 480p for faster generation, 720p for balance, 1080p for high quality, 4k for highest quality. |
| `seed` | опційне | integer / null | — | Random seed for reproducibility. Note that results may still vary slightly even with the same seed. |
| `draft` | опційне | boolean | false | Generate a draft preview at 480p, overriding resolution. Returns a draft_id for completing the draft at 1080p or 4k within 7 days. |
| `aspect_ratio` | опційне | auto \| 21:9 \| 16:9 \| 4:3 \| 1:1 \| 3:4 \| 9:16 | "auto" | The aspect ratio of the generated video. Use 16:9 for landscape, 9:16 for portrait/vertical, 1:1 for square, 21:9 for ultrawide cinematic, or auto to let the model decide. |
| `prompt` | опційне | string / null | — | The text prompt used to generate the video. |
| `codec` | опційне | auto \| H264 \| H265 | "auto" | 'auto' retains default video codec behaviour; 'H264' uses H.264; 'H265' uses H.265. |
| `bitrate_mode` | опційне | standard \| high | "standard" | Output bitrate mode. 'high' requests a higher-quality, larger-file encode from the model; 'standard' uses the default bitrate. |
| `audio_urls` | опційне | array[string] | — | Reference audio to guide video generation. Refer to them in the prompt as @Audio1, @Audio2, etc. Supported formats: MP3, WAV. Up to 10 files. Each file must be 1.8 to 30.2 seconds and no larger than 15 MB; combined duration must not exceed 30.2 seconds. |
| `image_urls` | опційне | array[string] | — | Reference images to guide video generation. Refer to them in the prompt as @Image1, @Image2, etc. Supported formats: JPG, PNG, WebP, BMP, TIFF, GIF, HEIC, HEIF. Max 30 MB per image. Up to 30 images. Total files across all modalities must not exceed 50. |
| `task` | опційне | auto \| reference \| editing \| extension | "reference" | The type of video generation task. Reference uses the supplied media as guidance. Editing modifies a reference video and automatically coerces aspect_ratio and duration to auto. Extension continues a reference video and automatically coerces aspect_ratio to auto. Auto leaves the task type unset so the model decides it from the prompt and references. |

Вихідні поля: `draft_id`, `seed`, `video`.

### minimax/h3-max/text-to-video

[Сторінка моделі](https://fal.ai/models/minimax/h3-max/text-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `resolution` | опційне | 480P \| 768P \| 1080P | "768P" | The native generation resolution, or 1080P latent refinement from a native 768P source. |
| `seed` | опційне | integer / null | — | Random seed. A random seed is selected when omitted. |
| `prompt_expansion_mode` | обов’язкове | string | "balanced" | How much effort to spend rewriting the prompt before generation. 'disabled' skips prompt expansion. 'balanced' returns in about a second. 'quality' spends up to ~30s on a richer prompt. |
| `enable_safety_checker` | опційне | boolean | true | If set to true, the safety checker will be enabled. |
| `aspect_ratio` | опційне | 21:9 \| 16:9 \| 4:3 \| 1:1 \| 3:4 \| 9:16 | "16:9" | The aspect ratio of the generated video. |
| `prompt` | обов’язкове | string, minLength=1, maxLength=50000 | — | Text prompt for video generation |
| `duration` | опційне | number, minimum=0.92, maximum=15 | 5 | Video length in seconds. The output can run up to about 0.7 s longer than requested. Use at least 2 s with target_audio_url. |
| `sync_mode` | опційне | boolean | false | Return the generated video as base64 instead of a CDN URL. |
| `target_audio_url` | опційне | string / null | — | Optional URL of an audio clip at least 2 seconds long (maximum 15 MB) to pin to the generated soundtrack. Longer clips are trimmed to the generated video's length, keeping the beginning. The original audio replaces the output soundtrack, padded with silence if shorter than the video, without changing playback speed. Exceptionally high sample rates may be resampled to 96 kHz. Accepts an HTTP(S) URL or a base64 data URI. |

Вихідні поля: `timings`, `expanded_prompt`, `video`.

### minimax/h3-max/image-to-video

[Сторінка моделі](https://fal.ai/models/minimax/h3-max/image-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `resolution` | опційне | 480P \| 768P \| 1080P | "768P" | The native generation resolution, or 1080P latent refinement from a native 768P source. |
| `end_image_url` | опційне | string / null | — | Optional URL of the image to use as the last frame. It may be provided alone for end-only keyframe generation; in that case the output canvas follows this image. |
| `prompt_expansion_mode` | обов’язкове | string | "balanced" | How much effort to spend rewriting the prompt before generation. 'disabled' skips prompt expansion. 'balanced' returns in about a second. 'quality' spends up to ~30s on a richer prompt. |
| `image_url` | опційне | string / null | — | Optional URL of the image to use as the first frame. When provided, the output canvas follows this image. If only end_image_url is provided, the canvas follows that last frame instead. If both images are omitted, the request is handled as text-to-video (16:9 by default). |
| `enable_safety_checker` | опційне | boolean | true | If set to true, the safety checker will be enabled. |
| `prompt` | обов’язкове | string, minLength=1, maxLength=50000 | — | Text prompt for video generation |
| `sync_mode` | опційне | boolean | false | Return the generated video as base64 instead of a CDN URL. |
| `duration` | опційне | number, minimum=0.92, maximum=15 | 5 | Video length in seconds. The output can run up to about 0.7 s longer than requested. Use at least 2 s with target_audio_url. |
| `target_audio_url` | опційне | string / null | — | Optional URL of an audio clip at least 2 seconds long (maximum 15 MB) to pin to the generated soundtrack. Longer clips are trimmed to the generated video's length, keeping the beginning. The original audio replaces the output soundtrack, padded with silence if shorter than the video, without changing playback speed. Exceptionally high sample rates may be resampled to 96 kHz. Accepts an HTTP(S) URL or a base64 data URI. |
| `seed` | опційне | integer / null | — | Random seed. A random seed is selected when omitted. |

Вихідні поля: `timings`, `expanded_prompt`, `video`.

### minimax/h3-max/reference-to-video

[Сторінка моделі](https://fal.ai/models/minimax/h3-max/reference-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `reference_audio_urls` | опційне | array[string], maxItems=3 | — | URLs of reference audio clips (2-15 seconds each, combined duration at most 15 seconds), referenced in the prompt as Audio 1, Audio 2, and so on. Images, videos, and audio can be provided individually or together. Reference images, videos, and audio clips must add up to at most 12 files. |
| `resolution` | опційне | 480P \| 768P \| 1080P | "768P" | The native generation resolution, or 1080P latent refinement from a native 768P source. |
| `seed` | опційне | integer / null | — | Random seed. A random seed is selected when omitted. |
| `image_url` | опційне | string / null | — | Optional URL of the image to use as the first frame. The video opens exactly on this image while the references keep the subjects consistent; the output canvas follows this image. |
| `aspect_ratio` | опційне | adaptive \| 21:9 \| 16:9 \| 4:3 \| 1:1 \| 3:4 \| 9:16 | "adaptive" | The aspect ratio of the generated video. |
| `duration` | опційне | number, minimum=0.92, maximum=15 | 5 | Video length in seconds. The output can run up to about 0.7 s longer than requested. Use at least 2 s with target_audio_url. |
| `middle_frame_time` | опційне | number / null | — | Target time for the middle image, in seconds from the start. Rounded to the nearest frame at 24 fps; it must fall strictly between the first and last frames of the requested duration. Requires middle_image_url. |
| `reference_conditions` | опційне | array[object {type, url}], maxItems=12 | — | Ordered reference list; cross-modality order is semantic and is preserved end-to-end. Do not combine with reference_*_urls. |
| `reference_image_urls` | опційне | array[string], maxItems=9 | — | URLs of subject/style reference images, referenced in the prompt as Image 1, Image 2, and so on. Reference images, videos, and audio clips must add up to at most 12 files. |
| `target_audio_url` | опційне | string / null | — | Optional URL of an audio clip at least 2 seconds long (maximum 15 MB) to pin to the generated soundtrack. Cannot be combined with reference audio. Longer clips are trimmed to the generated video's length, keeping the beginning; shorter clips are padded with silence. The clip is resampled to 32 kHz stereo and replaces the output soundtrack without changing playback speed. Accepts an HTTP(S) URL or a base64 data URI. |
| `reference_video_urls` | опційне | array[string], maxItems=3 | — | URLs of motion/reference video clips (2-15 seconds each, combined duration at most 15 seconds), referenced in the prompt as Video 1, Video 2, and so on. Reference images, videos, and audio clips must add up to at most 12 files. |
| `end_image_url` | опційне | string / null | — | Optional URL of the image to use as the last frame. The video ends exactly on this image. |
| `prompt_expansion_mode` | обов’язкове | string | "balanced" | How much effort to spend rewriting the prompt before generation. 'disabled' skips prompt expansion. 'balanced' returns in about a second. 'quality' spends up to ~30s on a richer prompt. |
| `enable_safety_checker` | опційне | boolean | true | If set to true, the safety checker will be enabled. |
| `middle_image_url` | опційне | string / null | — | Optional image to guide the video at middle_frame_time. Requires start and end images and native 480P or 768P resolution. |
| `prompt` | обов’язкове | string, minLength=1, maxLength=50000 | — | Text prompt for video generation. Refer to reference assets by their modality and order in the reference lists: Image 1, Image 2, Video 1, Audio 1, and so on. |
| `sync_mode` | опційне | boolean | false | Return the generated video as base64 instead of a CDN URL. |

Вихідні поля: `timings`, `expanded_prompt`, `reference_tokens`, `seed`, `video`.

### google/gemini-omni-flash/v1.2/image-to-video

[Сторінка моделі](https://fal.ai/models/google/gemini-omni-flash/v1.2/image-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `image_url` | обов’язкове | string | — | URL of the first frame to animate. |
| `aspect_ratio` | опційне | 16:9 \| 9:16 | "16:9" | The aspect ratio of the generated video. |
| `prompt` | обов’язкове | string, maxLength=20000 | — | The text prompt describing how the first image should be animated or interpolated into the optional end image. |
| `duration` | опційне | integer, minimum=3, maximum=15 | 8 | The duration of the generated video, in seconds. At most 10 seconds when an end image is provided. |
| `resolution` | опційне | 360p \| 720p \| 1080p \| 4k | "720p" | The resolution of the generated video. |
| `end_image_url` | опційне | string / null | — | Optional URL of the end frame. When provided, the model interpolates between the two images in their listed order and the duration is capped at 10 seconds. |

Вихідні поля: `video`.

### xai/grok-imagine-video/v1.5/reference-to-video

[Сторінка моделі](https://fal.ai/models/xai/grok-imagine-video/v1.5/reference-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `resolution` | опційне | 480p \| 720p | "480p" | Resolution of the output video. |
| `reference_image_urls` | обов’язкове | array[string], minItems=1, maxItems=7 | — | One or more reference image URLs to guide the video generation as style and content references. Reference in prompt as <IMAGE_0>, <IMAGE_1>, etc. Maximum 7 images. |
| `enable_safety_checker` | опційне | boolean | true | Authorized callers may set false to request relaxed screening. |
| `prompt` | обов’язкове | string, maxLength=4096 | — | Text prompt describing the video. Tag references as <IMAGE_0>, <IMAGE_1>, etc. |
| `duration` | опційне | integer, minimum=1, maximum=15 | 8 | Video duration in seconds. |
| `aspect_ratio` | опційне | 16:9 \| 4:3 \| 3:2 \| 1:1 \| 2:3 \| 3:4 \| 9:16 | "16:9" | Aspect ratio of the generated video. |

Вихідні поля: `video`.

### alibaba/happy-horse/v1.1/reference-to-video

[Сторінка моделі](https://fal.ai/models/alibaba/happy-horse/v1.1/reference-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `enable_safety_checker` | опційне | boolean | true | Enable content moderation for input and output. Disabling it requires account authorization; unauthorized requests are always checked. |
| `aspect_ratio` | опційне | 16:9 \| 9:16 \| 1:1 \| 4:3 \| 3:4 \| 21:9 \| 9:21 \| 5:4 \| 4:5 | "16:9" | Aspect ratio of the generated video. |
| `prompt` | обов’язкове | string, minLength=1 | — | Text prompt describing the desired video. Reference subjects from your images using ``character1``, ``character2``, ... up to ``character9`` (the order matches the order of ``image_urls``). Max 2500 characters. |
| `image_urls` | обов’язкове | array[string] | — | Reference images for subject consistency (1-9 images). Formats: JPEG, JPG, PNG, WEBP. Shortest side must be at least 400 px (720P or higher recommended). Max 20 MB each. |
| `duration` | опційне | 3 \| 4 \| 5 \| 6 \| 7 \| 8 \| 9 \| 10 \| 11 \| 12 \| 13 \| 14 \| 15 | 5 | Output video duration in seconds (3-15). |
| `resolution` | опційне | 720p \| 1080p | "1080p" | Output video resolution tier. |
| `seed` | опційне | integer / null | — | Random seed for reproducibility (0-2147483647). |

Вихідні поля: `seed`, `video`.

### fal-ai/veo3.1/first-last-frame-to-video

[Сторінка моделі](https://fal.ai/models/fal-ai/veo3.1/first-last-frame-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `generate_audio` | опційне | boolean | true | Whether to generate audio for the video. |
| `negative_prompt` | опційне | string / null | — | A negative prompt to guide the video generation. |
| `prompt` | обов’язкове | string, maxLength=20000 | — | The text prompt describing the video you want to generate |
| `resolution` | опційне | 720p \| 1080p \| 4k | "720p" | The resolution of the generated video. |
| `last_frame_url` | обов’язкове | string | — | URL of the last frame of the video |
| `seed` | опційне | integer / null | — | The seed for the random number generator. |
| `aspect_ratio` | опційне | auto \| 16:9 \| 9:16 | "auto" | The aspect ratio of the generated video. |
| `auto_fix` | опційне | boolean | false | Whether to automatically attempt to fix prompts that fail content policy or other validation checks by rewriting them. |
| `first_frame_url` | обов’язкове | string | — | URL of the first frame of the video |
| `safety_tolerance` | опційне | 1 \| 2 \| 3 \| 4 \| 5 \| 6 | "4" | The safety tolerance level for content moderation. 1 is the most strict (blocks most content), 6 is the least strict. |
| `duration` | опційне | 4s \| 6s \| 8s | "8s" | The duration of the generated video. |

Вихідні поля: `video`.

### lightricks/ltx-2.5/audio-to-video/pro

[Сторінка моделі](https://fal.ai/models/lightricks/ltx-2.5/audio-to-video/pro)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `prompt` | опційне | string / null | — | Text description of how the video should be generated. Required if image_url is not provided. When image_url is provided, this describes how the image should be animated. |
| `enable_safety_checker` | опційне | boolean | true | Authorized callers may set false to request relaxed screening. |
| `aspect_ratio` | опційне | auto \| 16:9 \| 9:16 | "auto" | The aspect ratio of the generated video. If 'auto', the aspect ratio will be determined automatically based on the input image, or defaults to 16:9 if no image is provided. |
| `audio_url` | обов’язкове | string | — | URL of the audio file to generate a video from. Duration must be between 2 and 20 seconds; pro models support a maximum of 10 seconds. Must be publicly accessible or base64 data URI. |
| `image_url` | опційне | string / null | — | URL of an image to use as the first frame of the video. If not provided, prompt is required. |

Вихідні поля: `video`.

## AI-редагування відео

### google/gemini-omni-flash/v1.2/edit

[Сторінка моделі](https://fal.ai/models/google/gemini-omni-flash/v1.2/edit)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `prompt` | обов’язкове | string, maxLength=20000 | — | A simple instruction describing the edit. |
| `resolution` | опційне | 360p \| 720p \| 1080p \| 4k | "720p" | The resolution of the edited video. |
| `video_url` | обов’язкове | string | — | URL of the video to edit. Must be at most 15 seconds long. |

Вихідні поля: `video`.

### xai/grok-imagine-video/edit-video

[Сторінка моделі](https://fal.ai/models/xai/grok-imagine-video/edit-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `resolution` | опційне | auto \| 480p \| 720p | "auto" | Resolution of the output video. |
| `enable_safety_checker` | опційне | boolean | true | Authorized callers may set false to request relaxed screening. |
| `prompt` | обов’язкове | string, maxLength=4096 | — | Text description of the desired edit. |
| `video_url` | обов’язкове | string | — | URL of the input video to edit. The video will be resized to a maximum area of 854x480 pixels and truncated to 8 seconds. |

Вихідні поля: `video`.

### minimax/h3-max/recast

[Сторінка моделі](https://fal.ai/models/minimax/h3-max/recast)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `enable_safety_checker` | опційне | boolean | true | Authorized callers may set false to request relaxed screening. |
| `reference_image_urls` | обов’язкове | array[string], minItems=1, maxItems=4 | — | One photo per new person. By default they replace the main people in the video from left to right, each in every shot they appear in. |
| `enhance_realism` | опційне | boolean | false | More natural skin textures and better blending of the new people into the scene. Off unless set. |
| `seed` | опційне | integer / null | — | Random seed. Leave empty for a random one. |
| `resolution` | опційне | 768P \| 1080P | "1080P" |  |
| `video_url` | обов’язкове | string | — | The source video, 5 to 30 seconds long, with no single shot longer than 15 seconds. |
| `prompt` | опційне | string / null | — | Optional: who becomes whom, or what else to keep or change. |

Вихідні поля: `video`, `seed`.

### minimax/h3-max/reframe-video

[Сторінка моделі](https://fal.ai/models/minimax/h3-max/reframe-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `enable_safety_checker` | опційне | boolean | true |  |
| `aspect_ratio` | опційне | 16:9 \| 9:16 \| 1:1 \| 4:3 \| 3:4 \| 21:9 \| 9:21 | "16:9" | Target canvas aspect ratio; the source is contain-fitted and the rest is outpainted. |
| `prompt` | опційне | string, maxLength=50000 | "" | Optional guidance for the new surroundings. Expansion captions the source automatically. |
| `resolution` | опційне | 480p \| 768p \| 1080p | "768p" | Target canvas resolution profile. 1080p uses learned latent upscaling from a native 768p reframe. |
| `video_url` | обов’язкове | string | — | Source video, 0.25 to 300 seconds; fitted onto the target canvas with its timeline and audio preserved. |
| `seed` | опційне | integer / null | — |  |

Вихідні поля: `frame_count`, `seed`, `expanded_prompt`, `placement`, `frames_per_second`, `video`.

### minimax/h3-max/relight

[Сторінка моделі](https://fal.ai/models/minimax/h3-max/relight)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `enable_safety_checker` | опційне | boolean | true | Enable safety checking. |
| `aspect_ratio` | опційне | adaptive \| 21:9 \| 16:9 \| 4:3 \| 1:1 \| 3:4 \| 9:16 | "16:9" | Output video aspect ratio. |
| `video_url` | обов’язкове | string, minLength=1 | — | Source video up to 15 seconds long. Converted to constant 24 fps and trimmed at the end to the closest 17n+5 frame count, with at least 56 frames (about 2.33 seconds) remaining. The output matches this prepared video's frame count and duration. |
| `sync_mode` | опційне | boolean | false | Return video as a data URI. |
| `resolution` | опційне | 480P \| 768P \| 1080P \| 2K | "768P" | Output video resolution. 480P and 768P generate natively; 1080P and 2K (1440p) use latent upscaling and refinement from 768P. |
| `reference_image_url` | обов’язкове | string, minLength=1 | — | Sphere render showing the target lighting. |
| `seed` | опційне | integer / null | — | Random seed for video generation. |

Вихідні поля: `timings`, `seed`, `video`.

### minimax/h3-max/extend-video

[Сторінка моделі](https://fal.ai/models/minimax/h3-max/extend-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `reference_audio_urls` | опційне | array[string], maxItems=3 | — | Optional audio references for the continuation (2–15 seconds each, 15 seconds combined). The full extended video retains its original source soundtrack, and its ending still conditions the transition. These clips guide the newly generated audio instead of using that soundtrack as an audio reference. Assign each clip a role in the prompt, such as 'Audio 1 for the voice' and 'Audio 2 for background music'. |
| `output` | опційне | extended \| continuation | "extended" | 'extended' returns the source and new footage as one video. 'continuation' returns a clip that starts with a 1.625-second repeat of the source's ending, then shows the new footage. |
| `resolution` | опційне | 480P \| 768P \| 1080P \| 2K | "768P" | Output video resolution. |
| `video_url` | обов’язкове | string, minLength=1 | — | URL of the video to extend. Must be 1.625 s to 60 s long, up to 50 MB, aspect ratio between 0.4 and 2.5. |
| `enable_prompt_expansion` | опційне | boolean | true | Automatically enhance the prompt using the source video to help keep the continuation consistent. May increase processing time. |
| `enable_safety_checker` | опційне | boolean | true | Moderate the source video and the prompt. |
| `aspect_ratio` | опційне | auto \| 21:9 \| 16:9 \| 4:3 \| 1:1 \| 3:4 \| 9:16 | "auto" | Output aspect ratio. 'auto' follows the source video. Other values crop the video to fit the selected ratio. |
| `prompt` | обов’язкове | string, minLength=1, maxLength=50000 | — | What happens next. Describe the continuation, not the source. |
| `duration` | опційне | number, minimum=0.71, maximum=15 | 5 | Seconds of new footage to add. The continuation clip also includes 1.625 seconds from the source's ending and may be longer because of frame rounding. |
| `seed` | опційне | integer / null | — | Seed for the continuation. Random when omitted. |

Вихідні поля: `timings`, `expanded_prompt`, `source`, `duration`, `seed`, `video`.

### bria/video/erase/mask

[Сторінка моделі](https://fal.ai/models/bria/video/erase/mask)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `video_url` | обов’язкове | string | — | Input video to erase object from. duration must be less than 5s. |
| `mask_video_url` | обов’язкове | string | — | Input video to mask erase object from. duration must be less than 5s. |
| `auto_trim` | опційне | boolean | true | auto trim the video, to working duration ( 5s ) |
| `preserve_audio` | опційне | boolean | true | If true, audio will be preserved in the output video. |
| `output_container_and_codec` | опційне | mp4_h265 \| mp4_h264 \| webm_vp9 \| gif \| mov_h264 \| mov_h265 \| mov_proresks \| mkv_h264 \| mkv_h265 \| mkv_vp9 \| mkv_mpeg4 | "mp4_h264" | Output container and codec. Options: mp4_h265, mp4_h264, webm_vp9, gif, mov_h264, mov_h265, mov_proresks, mkv_h264, mkv_h265, mkv_vp9, mkv_mpeg4. |

Вихідні поля: `video`.

### pixelcut/video-background-removal

[Сторінка моделі](https://fal.ai/models/pixelcut/video-background-removal)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `output_format` | опційне | webm_vp9 \| mp4_h264 \| mp4_h265 \| mov_proresks \| mov_h265 \| mkv_h264 \| mkv_h265 \| mkv_vp9 \| gif / null | — | Output video format. Auto-detected if not set (defaults to webm_vp9 for transparent). Transparent backgrounds need webm_vp9, mov_h265, mov_proresks, mkv_vp9 or gif. Transparent MOV is meant for Apple players and editing tools; browser previews, especially Chrome, may show edge halos or no transparency. Use webm_vp9 for transparent web playback. |
| `background` | опційне | transparent \| black \| white \| green \| blue \| magenta \| custom | "transparent" | Output background: transparent, a named preset color, or 'custom' to use the background_color color picker. |
| `video_url` | обов’язкове | string | — | URL of the input video |
| `background_color` | опційне | object {b, r, g} | — | Custom solid background color (only used when background='custom'). |

Вихідні поля: `video`.

### topaz/upscale/video/precision

[Сторінка моделі](https://fal.ai/models/topaz/upscale/video/precision)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `recover_detail` | опційне | number / null | — | Recover original detail level (0.0-1.0). Higher values preserve more original detail. |
| `enable_safety_checker` | опційне | boolean | true |  |
| `video_url` | обов’язкове | string | — | URL of the video to upscale |
| `compression` | опційне | number / null | — | Compression artifact removal level (0.0-1.0). Default varies by model. |
| `model` | опційне | Proteus \| Proteus Natural \| Iris \| Iris Low Quality \| Dione DV \| Dione TV \| Dione Robust \| Dione Dehalo \| Dione Robust Dehalo \| Artemis High Quality \| Artemis Medium Quality \| Artemis Low Quality \| Artemis Strong Halo \| Artemis Medium Halo \| Artemis Aliasing & Moire \| Gaia HQ \| Gaia CG \| Gaia 2 \| Rhea \| Theia Fine Tune Detail \| Theia Fine Tune Fidelity | "Proteus" | Precision (non-generative) enhancement model. Proteus fits most real-world footage; Proteus Natural is a softer variant; Iris recovers faces; Dione deinterlaces legacy/interlaced sources; Artemis denoises and sharpens degraded footage; Gaia refines high-quality footage and CG (Gaia 2 upscales animation at 2x); Rhea maximizes fine detail via an internal 4x pass; Theia gives manual detail/fidelity control. |
| `halo` | опційне | number / null | — | Halo reduction level (0.0-1.0). Default varies by model. |
| `noise` | опційне | number / null | — | Noise reduction level (0.0-1.0). Default varies by model. |
| `H264_output` | опційне | boolean | false | Whether to use H264 codec for output video. Default is H265. |
| `grain` | опційне | number / null | — | Film grain amount (0.0-0.1). Default varies by model. |
| `upscale_factor` | опційне | number, minimum=1, maximum=4 | 2 | Factor to upscale the video by (e.g. 2.0 doubles width and height) |
| `target_fps` | опційне | integer / null | — | Target FPS for the output. Frame interpolation is enabled only when this differs from the source FPS. |

Вихідні поля: `video`.

### topaz/interpolate/video

[Сторінка моделі](https://fal.ai/models/topaz/interpolate/video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `slowdown_factor` | опційне | integer, minimum=1, maximum=8 | 1 | Slow-motion factor: 2 makes the output twice as long at the target FPS (2x slow motion), up to 8x. 1 keeps the original speed. The extra generated frames are billed like interpolated frames. |
| `H264_output` | опційне | boolean | false | Whether to use H264 codec for output video. Default is H265. |
| `enable_safety_checker` | опційне | boolean | true |  |
| `video_url` | обов’язкове | string | — | URL of the video to retime / interpolate |
| `model` | опційне | Apollo \| Chronos \| Aion | "Apollo" | Frame interpolation model. Apollo is general-purpose; Chronos targets real-world motion; Aion handles extreme/complex motion. |
| `target_fps` | опційне | integer, minimum=16, maximum=120 | 60 | Target frames per second for the interpolated output. |

Вихідні поля: `video`.

## Мова, Foley та аналіз

### fal-ai/sync-lipsync/v3

[Сторінка моделі](https://fal.ai/models/fal-ai/sync-lipsync/v3)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `video_url` | обов’язкове | string | — | URL of the input video |
| `sync_mode` | опційне | cut_off \| loop \| bounce \| silence \| remap | "cut_off" | Lipsync mode when audio and video durations are out of sync. |
| `audio_url` | обов’язкове | string | — | URL of the input audio |
| `options` | опційне | object {temperature, occlusion_detection_enabled, active_speaker_detection, prompt, model_mode, sync_mode} / null | — | Additional Sync.so generation options. If options.sync_mode is set, it overrides the top-level sync_mode field. |
| `enable_safety_checker` | опційне | boolean | true |  |

Вихідні поля: `video`.

### heygen/avatar-6/image-to-video

[Сторінка моделі](https://fal.ai/models/heygen/avatar-6/image-to-video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `resolution` | опційне | 1080p \| 2k | "1080p" | Output resolution. |
| `image_url` | обов’язкове | string | — | URL of a photo of the person to animate. |
| `motion_prompt` | опційне | string / null | — | Optional direction for the avatar's motion and expression. |
| `enable_safety_checker` | опційне | boolean | true | Authorized callers may set false to request relaxed screening. |
| `audio_url` | обов’язкове | string | — | URL of the speech audio. It sets the video length. |

Вихідні поля: `video`.

### veed/dubbing/pro

[Сторінка моделі](https://fal.ai/models/veed/dubbing/pro)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `target_language` | обов’язкове | af \| ak \| am \| ar \| ar-EG \| as \| az \| be \| bg \| bo \| bs \| ca \| ceb \| cmn \| cs \| cy \| da \| de \| dgo \| el \| en \| en-AU \| en-CA \| en-GB \| en-US \| es \| es-AR \| es-CL \| es-ES \| es-MX \| et \| eu \| fa \| fi \| fil \| fr \| fr-CA \| fr-FR \| gl \| gu \| ha \| he \| hi \| hr \| hu \| hy \| id \| is \| it \| ja \| jv \| ka \| ki \| kk \| kn \| ko \| ky \| lg \| lt \| lv \| mk \| ml \| mn \| mr \| ms \| my \| ne \| nl \| no \| nso \| pa \| pl \| pt \| pt-BR \| pt-PT \| rn \| ro \| ru \| rw \| sd \| sk \| sl \| sq \| ss \| st \| su \| sv \| sw \| ta \| te \| tg \| th \| tn \| tr \| ts \| ug \| uk \| ur \| uz \| ve \| vi \| war \| wo \| yo \| yue \| zh \| zh-TW \| zu | — | Language to dub into, optionally with a regional dialect (e.g. 'es-MX', 'pt-BR'). Case-insensitive; for a language without dialects the region is ignored ('de-DE' = 'de'), and an unsupported dialect is rejected. |
| `keyterms` | опційне | array[string], maxItems=1000 | [] | Names and terms to get right in the dub, such as brand, product or people's names: they help the speech recognition catch these words and the translation keep them as written. Up to 1,000 terms, each at most 50 characters and 5 words, without the characters < > { } [ ] \. |
| `video_url` | обов’язкове | string, minLength=1, maxLength=2083 | — | Video to dub, 8 seconds to 10 minutes long and with speech in its audio track. The speech is translated into the target language, and the speakers' lips are synced to the dubbed voices. |
| `voice_cloning_strength` | опційне | integer, minimum=0, maximum=10 | 7 | How closely the dubbed voices match the original speakers, from 0 to 10. Higher keeps more of each speaker's voice and accent; lower sounds more natural in the target language. |
| `source_language` | опційне | auto \| af \| ak \| am \| ar \| as \| az \| be \| bg \| bo \| bs \| ca \| ceb \| cmn \| cs \| cy \| da \| de \| dgo \| el \| en \| es \| et \| eu \| fa \| fi \| fil \| fr \| gl \| gu \| ha \| he \| hi \| hr \| hu \| hy \| id \| is \| it \| ja \| jv \| ka \| ki \| kk \| kn \| ko \| ky \| lg \| lt \| lv \| mk \| ml \| mn \| mr \| ms \| my \| ne \| nl \| no \| nso \| pa \| pl \| pt \| rn \| ro \| ru \| rw \| sd \| sk \| sl \| sq \| ss \| st \| su \| sv \| sw \| ta \| te \| tg \| th \| tn \| tr \| ts \| ug \| uk \| ur \| uz \| ve \| vi \| war \| wo \| yo \| yue \| zh \| zu | "auto" | Language spoken in the video. 'auto' (the default) detects it; set it explicitly if detection picks the wrong language. |

Вихідні поля: `video`.

### fal-ai/elevenlabs/speech-to-text/scribe-v2

[Сторінка моделі](https://fal.ai/models/fal-ai/elevenlabs/speech-to-text/scribe-v2)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `keyterms` | опційне | array[string], maxItems=100 | [] | Words or sentences to bias the model towards transcribing. Up to 100 keyterms, max 50 characters each. Adds 30% premium over base transcription price. |
| `tag_audio_events` | опційне | boolean | true | Tag audio events like laughter, applause, etc. |
| `language_code` | опційне | string / null | — | Language code of the audio |
| `diarize` | опційне | boolean | true | Whether to annotate who is speaking |
| `audio_url` | обов’язкове | string | — | URL of the audio file to transcribe |

Вихідні поля: `words`, `text`, `language_probability`, `language_code`.

### fal-ai/elevenlabs/forced-alignment

[Сторінка моделі](https://fal.ai/models/fal-ai/elevenlabs/forced-alignment)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `text` | обов’язкове | string, minLength=1, maxLength=675000 | — | Transcript to align with the audio |
| `audio_url` | обов’язкове | string | — | URL of the audio file to align. The file can be up to 3 GB and the audio can be up to 10 hours long. |

Вихідні поля: `words`, `characters`, `loss`.

### mirelo-ai/sfx2.0/video-to-audio

[Сторінка моделі](https://fal.ai/models/mirelo-ai/sfx2.0/video-to-audio)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `negative_prompt` | опційне | string / null | — | Sounds to keep out of the result, as a short comma-separated list. |
| `return_speech` | опційне | boolean | false | Also return the input's separated speech as its own audio file, in the response's speech. With preserve_speech false the soundtracks are sound effects only and the speech is separated while they generate. With preserve_speech true it is the speech separated from the input that the soundtracks were generated around, not the speech in them: the model renders that speech anew, so the file does not cancel or double it cleanly when layered onto a soundtrack. The file is mono, in upload_audio_format, and as long as the soundtracks. It is not billed. |
| `video_url` | обов’язкове | string | — | Video to add sound to: an http(s) URL, or a base64 data URI up to 8 MB. |
| `num_samples` | опційне | integer, minimum=1, maximum=4 | 2 | Number of variations to generate. Billed per sample. |
| `upload_audio_bitrate_kbps` | опційне | integer / null | — | Bitrate in kbps for an mp3 or aac upload. mp3 is written at exactly this constant rate, one of 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320. aac takes 32 to 256 as a target the encoder may undershoot on mono or sparse audio. Unset keeps the default: mp3 at LAME V0 VBR, aac at a 256 kbps target. Refused with a lossless upload_audio_format. |
| `seed` | опційне | integer / null | — | Seed for generation. -1 or None for random. |
| `text_prompt` | опційне | string / null | — | Optional text guiding the soundtrack. Name sounds the picture does not show, such as off-screen sounds or an ambience bed, to have them worked into it. |
| `preserve_speech` | опційне | boolean | true | Keep the speech in the input's audio and generate the rest of the soundtrack around it. False generates sound effects only and suppresses speech. |
| `duration` | опційне | number, minimum=1, maximum=600 | 10 | Seconds of sound to generate, from 1 s to 600 s, clamped to the video's length. Over 10 s generates in 10 s windows. A video shorter than 1 s answers 400. |
| `upload_audio_format` | опційне | wav \| mp3 \| aac \| flac | "wav" | Audio format of each file |

Вихідні поля: `audio`, `model`, `speech`.

### sonilo/v1.1/video-to-sound-effects

[Сторінка моделі](https://fal.ai/models/sonilo/v1.1/video-to-sound-effects)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `audio_format` | опційне | wav \| mp3 \| aac \| flac | "aac" | Format of the returned audio file: aac (default), mp3, wav, or flac. (The video with sound is always AAC.) |
| `prompt` | опційне | string / null | — | Optional. Describe the kind of sound you want; it steers the generated audio for every scene. Leave empty to caption the video automatically. |
| `video_url` | обов’язкове | string | — | The video to add sound to (public URL, or upload a file). The generated audio matches the video's length. |
| `keep_speech_vocal` | опційне | boolean | false | Keep the original video's speech/vocals. When on, the source audio is separated (music source separation) and the isolated vocals are kept as recorded, with the generated sound mixed in at a level matched to the voice; the rest of the original soundtrack (music, ambience) is dropped. Applies to the returned audio and video. When off (default), the result carries only the generated sound. |
| `segments` | опційне | array[object {start, prompt, end}] / null | — | Optional. Split the video into time ranges, each with its own sound description. Leave empty to split into scenes automatically. |

Вихідні поля: `audios`, `audio`, `segments`.

### mureka/v9.5/generate/soundtrack

[Сторінка моделі](https://fal.ai/models/mureka/v9.5/generate/soundtrack)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `video_id` | опційне | string / null | — | Video ID returned by /files/upload with purpose='soundtrack'. Provide exactly one of image_id or video_id. |
| `audio_start` | опційне | integer / null | — | Start time of the soundtrack audio in milliseconds. If only audio_start is specified, generation starts there and continues for the video duration, stopping at the end of the song if the remaining audio is shorter. The soundtrack audio segment must be at least 3 seconds long, and a 1-second fade-in is added at the beginning. |
| `enable_safety_checker` | опційне | boolean | true | Authorized callers may set false to request relaxed screening. |
| `prompt` | опційне | string / null | — | Optional description of the desired soundtrack style and mood. |
| `audio_end` | опційне | integer / null | — | End time of the soundtrack audio in milliseconds. If both audio_start and audio_end are specified, generation uses those times. If audio_end exceeds the song duration, generation stops at the end of the song. The soundtrack audio segment must be at least 3 seconds long, and a 1-second fade-out is added at the end. |
| `image_id` | опційне | string / null | — | Image ID returned by /files/upload with purpose='soundtrack'. Provide exactly one of image_id or video_id. |

Вихідні поля: `song_id`, `lyrics_sections`, `duration`, `audio`.

### fal-ai/sam-audio/visual-separate

[Сторінка моделі](https://fal.ai/models/fal-ai/sam-audio/visual-separate)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `output_format` | опційне | wav \| mp3 | "wav" | Output audio format. |
| `reranking_candidates` | опційне | integer, minimum=1, maximum=4 | 1 | Number of candidates to generate and rank. Higher improves quality but increases latency and cost. |
| `mask_video_url` | опційне | string / null | — | URL of the mask video (binary mask indicating target object). Black=target, White=background. |
| `acceleration` | опційне | fast \| balanced \| quality | "balanced" | The acceleration level to use. |
| `video_url` | обов’язкове | string | — | URL of the video file to process (MP4, MOV, etc.) |
| `max_chunk_duration` | опційне | number, minimum=10, maximum=60 | 60 | Maximum audio duration (in seconds) to process in a single pass. Longer audio will be chunked with overlap and blended. |
| `prompt` | опційне | string | "" | Text prompt to assist with separation. Use natural language to describe the target sound. |
| `chunk_overlap` | опційне | number, minimum=0, maximum=30 | 5 | Overlap duration (in seconds) between chunks for crossfade blending. |

Вихідні поля: `sample_rate`, `target`, `duration`, `residual`.

### nvidia/nemotron-3-5-super/video

[Сторінка моделі](https://fal.ai/models/nvidia/nemotron-3-5-super/video)

| Поле | Вимога | Тип і межі | Default | Опис схеми |
| --- | --- | --- | --- | --- |
| `reasoning_mode` | опційне | think \| no_think | "no_think" | `think` emits an explicit reasoning trace before the final answer; `no_think` returns a direct answer. |
| `prompt` | обов’язкове | string, minLength=1 | — | Text prompt to send to the model. |
| `top_p` | опційне | number, maximum=1 | 0.95 | Nucleus sampling probability mass. |
| `max_tokens` | опційне | integer, minimum=1, maximum=32000 | 1024 | Maximum number of tokens to generate. |
| `system_prompt` | опційне | string / null | — | Optional system prompt to steer the model. |
| `temperature` | опційне | number, minimum=0, maximum=2 | 1 | Sampling temperature. NVIDIA recommends 1.0 for all tasks. |
| `enable_safety_checker` | опційне | boolean | true | Whether to enable the safety checker. |
| `video_url` | обов’язкове | string | — | URL of the video to reason about. mp4, max 2 minutes, max 3840 pixels per side and 3840x2160 total pixels. |

Вихідні поля: `finish_reason`, `reasoning`, `usage`, `output`.
