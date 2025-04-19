#version 330 core 

out vec4 out_color;

uniform vec4 light_color;

void main() {
    out_color = light_color;
}