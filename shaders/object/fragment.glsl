#version 330 core 

in vec2 v_tex_cord;

out vec4 out_color;

uniform sampler2D texture1;
uniform vec4 light_color;

void main() {
    out_color = texture(texture1, v_tex_cord) * light_color;
}