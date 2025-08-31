#version 330
uniform sampler2D surface;
uniform sampler2D ui_surf;
uniform sampler2D bg_surf;
uniform float time;
uniform float tremor = 0.015;
uniform vec2 resolution = vec2(1280, 960);
uniform bool pixelate = false;
uniform float noise_opacity = 0.7;
uniform float noise_speed = 4.0;
uniform float static_noise_intensity = 0.05;
uniform float aberration = 0.015;
uniform float brightness = 1.4;
uniform float desaturation = 0.8;
uniform float vignette_intensity = 1.5;
uniform float vignette_opacity = 0.8;
uniform float scanlines_opacity = 0.15;
uniform float flicker_intensity = 0.02;
uniform float bloom_threshold = 0.75;
uniform float bloom_intensity = 0.2;
uniform float color_bleed = 0.005;
uniform float phosphor_decay = 0.2;
uniform float film_grain_scale = 600.0;
out vec4 f_color;
in vec2 uv;

vec3 hash33(vec3 p) {
    p = fract(p * vec3(0.1031, 0.1030, 0.0973));
    p += dot(p, p.yxz + 33.33);
    return fract((p.xxy + p.yxx) * p.zyx);
}

float perlin_noise(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);
    vec3 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(mix(dot(hash33(i + vec3(0,0,0)), f - vec3(0,0,0)),
                       dot(hash33(i + vec3(1,0,0)), f - vec3(1,0,0)), u.x),
                   mix(dot(hash33(i + vec3(0,1,0)), f - vec3(0,1,0)),
                       dot(hash33(i + vec3(1,1,0)), f - vec3(1,1,0)), u.x), u.y),
               mix(mix(dot(hash33(i + vec3(0,0,1)), f - vec3(0,0,1)),
                       dot(hash33(i + vec3(1,0,1)), f - vec3(1,0,1)), u.x),
                   mix(dot(hash33(i + vec3(0,1,1)), f - vec3(0,1,1)),
                       dot(hash33(i + vec3(1,1,1)), f - vec3(1,1,1)), u.x), u.y), u.z);
}

float film_grain(vec2 uv, float t) {
    vec3 p = vec3(uv * film_grain_scale, t * 0.1);
    return perlin_noise(p) * 2.0 - 1.0;
}

vec2 apply_tremor(vec2 uv) {
    float shake = sin(time * 15.0) * cos(time * 11.0) * tremor;
    return uv + vec2(shake * sin(time * 3.0), shake * cos(time * 5.0));
}

float vignette(vec2 uv) {
    uv *= 1.0 - uv.yx;
    return pow(20.0 * uv.x * uv.y * (1.0 - uv.x) * (1.0 - uv.y), vignette_intensity * vignette_opacity);
}

vec3 bloom(vec3 color, float threshold, float intensity) {
    vec3 bright = max(color - threshold, 0.0);
    bright *= bright;
    return color + bright * intensity;
}

vec3 apply_phosphor(vec3 color, float decay) {
    return color * (1.0 - decay) + color * decay * sin(time * 20.0) * 0.05;
}

vec3 color_grade(vec3 color) {
    color = pow(color, vec3(1.1));
    color = mix(color, vec3(dot(color, vec3(0.3, 0.59, 0.11))), desaturation);
    color *= vec3(0.95, 0.9, 0.85); // Rusty tint for Silent Hill vibe
    return color;
}

void main() {
    vec4 ui_col = texture(ui_surf, uv);

    vec2 tex_uv = apply_tremor(uv);
    if (pixelate) {
        tex_uv = floor(tex_uv * resolution + 0.5) / resolution;
    }

    float ab = aberration;
    vec2 offset_r = vec2(ab * sin(time * 1.5), color_bleed * cos(time * 0.8));
    vec2 offset_b = vec2(ab * cos(time * 1.2), color_bleed * sin(time * 0.9));
    vec3 bg_r = texture(bg_surf, tex_uv + offset_r).rgb;
    vec3 bg_g = texture(bg_surf, tex_uv).rgb;
    vec3 bg_b = texture(bg_surf, tex_uv - offset_b).rgb;
    vec3 bg_color = vec3(bg_r.r, bg_g.g, bg_b.b);

    vec4 main_col = texture(surface, tex_uv);
    vec3 color = bg_color;
    if (main_col.a > 0.01) {
        color = main_col.rgb * main_col.a + bg_color * (1.0 - main_col.a);
    }

    float scanline = (sin(tex_uv.y * resolution.y * 3.14159 * 2.0 + time * 0.2) * 0.5 + 0.5) * scanlines_opacity;
    color *= 1.0 - scanline * 0.15;
    float grain_val = film_grain(tex_uv, time * noise_speed) * static_noise_intensity * noise_opacity;
    color += grain_val;
    color = bloom(color, bloom_threshold, bloom_intensity);
    color = apply_phosphor(color, phosphor_decay);
    color *= 1.0 + sin(time * 10.0) * flicker_intensity;
    color = color_grade(color);
    color *= brightness * vignette(tex_uv);
    color = clamp(color, 0.0, 1.0);

    if (ui_col.a > 0.01) {
        color = ui_col.rgb * ui_col.a + color * (1.0 - ui_col.a);
    }

    f_color = vec4(color, 1.0);
}