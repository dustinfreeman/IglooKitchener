import viz
import projector

class ShadowProjector(object):
	def __init__(self,kernel=9,alpha=0.8,size=256,pos=(0,10,0),euler=(0,90,0),area=[5,5],scene=viz.MainScene):

		#Create render texture
		self.shadowTex = viz.addRenderTexture(wrap=viz.CLAMP_TO_BORDER,borderColor=viz.WHITE)

		#Create render node to render shadow caster to texture
		self.shadowPass = viz.addRenderNode(scene=scene,size=[size,size],inheritView=False,autoClip=False)
		self.shadowPass.setClearColor(viz.WHITE)
		self.shadowPass.attachTexture(self.shadowTex)
		self.shadowPass.setScene(None)

		#Apply shader to render node so everything is black
		code = """
		#define I	%alpha%
		void main()
		{
			gl_FragColor = vec4(I,I,I,1.0);
		}
		"""
		shader = viz.addShader(frag=code.replace('%alpha%',str(1.0-alpha)))
		self.shadowPass.apply(shader,op=viz.OP_OVERRIDE)

		#Create projector for projecting shadow texture onto receivers
		self.texProj = projector.add(self.shadowTex,scene=scene,cubemap=False)

		#Save all render node passes
		self.passes = [self.shadowPass]

		#Setup render nodes to blur shadow texture
		if kernel:
			blur_source = """
			uniform sampler2D srcImage;
			void main(void)
			{
				vec4 color = vec4(0,0,0,0);
				%code%
				color.a = 1.0;
				gl_FragColor = color;
			}"""
			horz_source = 'color += texture2D( srcImage, gl_TexCoord[0].xy + vec2( %f, 0.0 ) ) * %f;'
			vert_source = 'color += texture2D( srcImage, gl_TexCoord[0].xy + vec2( 0.0, %f ) ) * %f;'

			#Calculate weight and offsets for blur code
			weights = []
			offsets = []
			mid = float(kernel - 1)
			kernel *= 2
			for i in xrange(0,kernel,2):
				offsets.append( ((i-mid) / 2.0) * (1.0 / size) )
				x = (i - mid) / mid
				weights.append( 0.05 + ((-(x*x) + 1.0) / 4.0) )

			#Normalize weights
			frac = 1.0 / sum(weights)
			weights = [ frac * x for x in weights ]

			#Create blur code for shaders
			horz_blur_code = []
			vert_blur_code = []
			for w,o in zip(weights,offsets):
				horz_blur_code.append(horz_source%(o,w))
				vert_blur_code.append(vert_source%(o,w))

			#Create shaders
			horzBlurShader = viz.addShader(frag=blur_source.replace('%code%','\n'.join(horz_blur_code)))
			vertBlurShader = viz.addShader(frag=blur_source.replace('%code%','\n'.join(vert_blur_code)))
			srcImageUniform = viz.addUniformInt('srcImage',0)

			#Render texture for ping-ponging
			tex2 = viz.addRenderTexture()

			"""
			Pass 2 renders the shadow texture onto a quad.
			The quad has a shader attached which blurs the texture horizontally.
			"""
			self.blurPass1 = viz.addRenderNode(scene=scene)
			self.blurPass1.setHUD(0,200,0,200,renderQuad=True)
			self.blurPass1.setSize(size,size)
			self.blurPass1.setBuffer(viz.RENDER_FBO)
			self.blurPass1.setOrder(viz.PRE_RENDER,1)
			self.blurPass1.attachTexture(tex2)
			self.blurPass1.texture(self.shadowTex)
			self.blurPass1.apply(horzBlurShader)
			self.blurPass1.apply(srcImageUniform)
			self.passes.append(self.blurPass1)

			"""
			Pass 3 renders the texture from pass 2 onto a quad.
			The quad has a shader attached which blurs the texture vertically.
			"""
			self.blurPass2 = viz.addRenderNode(scene=scene)
			self.blurPass2.setHUD(0,200,0,200,renderQuad=True)
			self.blurPass2.setSize(size,size)
			self.blurPass2.setBuffer(viz.RENDER_FBO)
			self.blurPass2.setOrder(viz.PRE_RENDER,2)
			self.blurPass2.attachTexture(self.shadowTex)
			self.blurPass2.texture(tex2)
			self.blurPass2.apply(vertBlurShader)
			self.blurPass2.apply(srcImageUniform)
			self.passes.append(self.blurPass2)

			#Remove texture/shader/uniforms (already applied)
			horzBlurShader.remove()
			vertBlurShader.remove()
			srcImageUniform.remove()
			tex2.remove()

		#Initialize shadow area/pos/euler
		self.setArea(area)
		self.setPosition(pos)
		self.setEuler(euler)

	def addCaster(self,node):
		"""Add a shadow caster node"""
		node.duplicate(viz.MainScene,self.shadowPass)

	def addReceiver(self,node,unit=1):
		"""Add a shadow receiver node"""
		self.texProj.affect(node,unit)

	def setPosition(self,pos):
		"""Set position of shadow projector"""
		self.shadowPass.setPosition(pos)
		self.texProj.setPosition(pos)

	def setEuler(self,euler):
		"""Set euler of shadow projector"""
		self.shadowPass.setEuler(euler)
		self.texProj.setEuler(euler)

	def setArea(self,area):
		"""Set [width,height] area of orthographic projection of shadow"""
		proj = viz.Matrix.ortho(-area[0]/2.0,area[0]/2.0,-area[1]/2.0,area[1]/2.0,0.1,1000)
		self.shadowPass.setProjectionMatrix(proj)
		self.texProj.ortho(area[0],area[1])

	def visible(self,mode):
		"""Enable shadow projector"""
		for p in self.passes:
			p.visible(mode)
		self.texProj.visible(mode)

	def remove(self):
		"""Permanently remove all resources"""
		for p in self.passes:
			p.remove(False)
		self.shadowTex.remove()
		self.texProj.remove()
