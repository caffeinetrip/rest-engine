#version 330
uniform sampler2D surface;
uniform sampler2D ui_surf;
uniform sampler2D bg_surf;
uniform float time;
uniform float tremor = 0.02;
uniform vec2 resolution = vec2(1280, 960);
uniform bool pixelate = true;
uniform float noise_opacity = 0.2;
uniform float noise_speed = 5.0;
uniform float static_noise_intensity = 0.04;
uniform float aberration = 0.015;
uniform float brightness = 0.95;
uniform float desaturation = 0.4;
uniform float vignette_intensity = 0.8;
uniform float vignette_opacity = 0.7;
uniform float scanlines_opacity = 0.3;
uniform float flicker_intensity = 0.015;

out vec4 f_color;
in vec2 uv;

// Оптимізована функція шуму
vec2 random(vec2 uv) {
    return fract(sin(vec2(dot(uv, vec2(127.1, 311.7)), dot(uv, vec2(269.5, 183.3)))) * 43758.5453);
}

float noise(vec2 uv) {
    vec2 i = floor(uv);
    vec2 f = fract(uv);
    vec2 u = f * f * (3.0 - 2.0 * f); // Кубічна інтерполяція
    return mix(mix(dot(random(i), f),
                   dot(random(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
               mix(dot(random(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
                   dot(random(i + vec2(1.0)), f - vec2(1.0)), u.x), u.y);
}

// Спрощений FBM
float fbm(vec2 uv) {
    float v = 0.0, a = 0.4;
    for (int i = 0; i < 3; ++i) {
        v += a * noise(uv);
        uv *= 2.0;
        a *= 0.5;
    }
    return v;
}

// Спрощений grain
float grain(vec2 uv, float t) {
    return fract(sin(dot(uv + t, vec2(12.9898, 78.233))) * 43758.5453);
}

// Легке тремтіння
vec2 apply_tremor(vec2 uv) {
    vec2 t = sin(time * vec2(25.0, 17.0)) * cos(time * vec2(13.0, 23.0));
    return uv + t * tremor;
}

// Віньєтка
float vignette(vec2 uv) {
    uv = uv * (1.0 - uv);
    return pow(uv.x * uv.y * 15.0, vignette_intensity * vignette_opacity);
}

void main() {
    // Застосування тремтіння
    vec2 tex_uv = apply_tremor(uv);

    // Пікселізація
    if (pixelate) {
        tex_uv = floor(tex_uv * resolution + 0.5) / resolution;
    }

    // Зчитування текстур
    vec4 base_color = texture(bg_surf, tex_uv);
    vec4 src_color = texture(surface, tex_uv);
    if (src_color.a > 0.5) base_color = src_color;

    vec4 ui_color = texture(ui_surf, tex_uv);
    if (ui_color.r > 0.0) base_color += ui_color;

    // Хроматична аберація
    vec4 tex;
    vec2 aber = vec2(aberration, 0.0);
    tex.r = texture(bg_surf, tex_uv + aber).r;
    tex.g = texture(bg_surf, tex_uv).g;
    tex.b = texture(bg_surf, tex_uv - aber).b;
    tex.a = 1.0;

    // Змішування з базовим кольором
    tex = mix(tex, base_color, 0.7);

    // Сканлайни
    if (scanlines_opacity > 0.0) {
        float scan = sin(tex_uv.y * resolution.y * 2.0) * scanlines_opacity;
        tex.rgb *= 1.0 - scan * 0.2;
    }

    // Шум і grain
    tex.rgb += grain(tex_uv, time * noise_speed) * static_noise_intensity;
    tex.rgb += fbm(tex_uv * 2.0 + time * 0.02) * noise_opacity;

    // Десатурація для депресивного стилю
    if (desaturation > 0.0) {
        float gray = dot(tex.rgb, vec3(0.299, 0.587, 0.114));
        tex.rgb = mix(tex.rgb, vec3(gray), desaturation);
    }

    // Мерехтіння та яскравість
    tex.rgb *= 1.0 + sin(time * 8.0) * flicker_intensity;
    tex.rgb = clamp(tex.rgb * brightness * vignette(tex_uv), 0.0, 1.0);

    // Легке тонове зміщення для холодної палітри
    tex.rgb = mix(tex.rgb, tex.rgb * vec3(0.95, 0.98, 1.05), 0.3);

    f_color = tex;
}