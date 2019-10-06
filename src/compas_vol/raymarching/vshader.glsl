#version 120

uniform mat4 p3d_ModelViewProjectionMatrix;

attribute vec4 p3d_Vertex;


void main(){
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
    