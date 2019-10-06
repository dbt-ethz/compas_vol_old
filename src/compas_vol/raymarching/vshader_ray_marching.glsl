#version 120

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrixInverseTranspose;

// uniform mat4 p3d_ModelViewMatrix;
// uniform mat4 p3d_ProjectionMatrix;
// uniform mat4 p3d_ProjectionMatrixInverse;
// uniform mat4 p3d_ProjectionMatrixTranspose;

attribute vec4 p3d_Vertex;

uniform mat4 trans_apiview_to_view;
// uniform mat4 trans_view_to_apiview;
// uniform mat4 trans_model_to_apiview;

//attribute vec4 p3d_Color;
// attribute vec3 p3d_Normal;
// attribute vec4 vertex;
// attribute vec4 color;

void main(){
    gl_Position =  vec4(p3d_Vertex[0], p3d_Vertex[1], 0., 1.);
}
    


        // gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
