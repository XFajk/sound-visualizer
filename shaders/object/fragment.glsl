#version 330 core 

in vec2 v_tex_cord;
in vec3 v_normal;
in vec3 v_pos;

out vec4 out_color;

uniform sampler2D texture1;

uniform vec4 light_color;
uniform vec3 light_pos;
uniform vec3 view_pos;

float ambient_strength = 0.1;
vec4 ambient = light_color * ambient_strength;

vec3 normal = normalize(v_normal);
vec3 light_dir = normalize(light_pos - v_pos);

float diff = max(dot(normal, light_dir), 0.0);
vec4 diffuse = diff * light_color;

void main() {
    out_color = texture(texture1, v_tex_cord) * (ambient + diffuse);
}