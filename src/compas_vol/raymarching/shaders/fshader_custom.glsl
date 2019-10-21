#version 120

uniform vec2 u_resolution;
uniform float osg_FrameTime;

void main(){  
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    vec2 uv = 2*(st - vec2(0.5, 0.5));
    gl_FragColor = vec4 (1.);

}