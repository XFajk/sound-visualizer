#version 330 core

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_normal;
layout(location = 2) in vec2 a_tex_cord;

out vec2 v_tex_cord;
out vec3 v_normal;
out vec3 v_pos;
out vec3 v_light_pos;

uniform vec3 light_pos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat3 normal_matrix;

void main() {
    gl_Position = projection * view * model * vec4(a_pos, 1.0);
    v_pos = vec3(view * model * vec4(a_pos, 1.0));
    v_normal = normal_matrix * a_normal; // Correct normal transformation
    v_light_pos = vec3(view * vec4(light_pos, 1.0)); // Transform light position to view space
    v_tex_cord = a_tex_cord;
}