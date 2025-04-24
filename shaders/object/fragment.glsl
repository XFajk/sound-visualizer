#version 330 core 

in vec2 v_tex_cord;
in vec3 v_normal;
in vec3 v_pos;
in vec3 v_light_pos;

out vec4 out_color;

uniform sampler2D texture1;

uniform vec4 light_color;

void main() {

    // calculating ambient
    float ambient_strength = 0.1;
    vec4 ambient = light_color * ambient_strength;

    // calculating diffuse
    vec3 normal = normalize(v_normal);
    vec3 light_dir = normalize(v_light_pos - v_pos);

    float diff = max(dot(normal, light_dir), 0.0);
    vec4 diffuse = diff * light_color;

    // calculating specular
    float specular_strength = 0.8;

    vec3 view_dir = normalize(-v_pos); // Assuming camera is at origin
    vec3 reflect_dir = reflect(-light_dir, normal); // Reflect light direction around normal

    float specular = pow(max(dot(view_dir, reflect_dir), 0.0), 64); // Shininess factor
    vec4 specular_color = specular_strength * specular * light_color;

    out_color = texture(texture1, v_tex_cord) * (ambient + diffuse + specular_color);
}