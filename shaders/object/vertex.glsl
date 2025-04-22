#version 330 core

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_normal;
layout(location = 2) in vec2 a_tex_cord;

out vec2 v_tex_cord;
out vec3 v_normal;
out vec3 v_pos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat3 normal_matrix;

void main() {
    gl_Position = projection * view * model * vec4(a_pos, 1.0);
    v_pos = vec3(model * vec4(a_pos, 1.0));
    v_normal = mat3(transpose(inverse(model))) * a_normal; // Correct normal transformation
    v_tex_cord = a_tex_cord;
}