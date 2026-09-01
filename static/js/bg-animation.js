/**
 * ResumeForge AI — Modern 3D Geometric Animated Background (Three.js r128)
 * Eye-catching 3D floating low-poly crystals, glowing wireframe geometries, and interactive parallax.
 */

(function () {
  'use strict';

  let scene, camera, renderer, animationFrameId;
  let shapes = [];
  let particleSystem = null;
  let mouseX = 0, mouseY = 0;
  let targetMouseX = 0, targetMouseY = 0;
  let isTabActive = true;
  let prefersReducedMotion = false;
  const canvasId = 'bg-canvas';

  function init3DBackground() {
    let canvas = document.getElementById(canvasId);
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = canvasId;
      document.body.prepend(canvas);
    }

    // Force strict fixed background positioning behind all UI
    canvas.style.position = 'fixed';
    canvas.style.top = '0px';
    canvas.style.left = '0px';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';
    canvas.style.display = 'block';

    if (typeof THREE === 'undefined') {
      console.warn('Three.js library not found.');
      return;
    }

    prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 1. Scene & Camera Setup
    scene = new THREE.Scene();
    const width = window.innerWidth;
    const height = window.innerHeight;

    camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.z = 32;

    // 2. WebGL Renderer
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

    // 3. Dynamic Scene Lighting
    const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.95);
    scene.add(ambientLight);

    const pointLightPrimary = new THREE.PointLight(0x4F46E5, 3.0, 120);
    pointLightPrimary.position.set(25, 30, 25);
    scene.add(pointLightPrimary);

    const pointLightSecondary = new THREE.PointLight(0x8B5CF6, 2.5, 120);
    pointLightSecondary.position.set(-25, -25, 20);
    scene.add(pointLightSecondary);

    const pointLightCyan = new THREE.PointLight(0x06B6D4, 2.2, 100);
    pointLightCyan.position.set(0, 35, 15);
    scene.add(pointLightCyan);

    // 4. Materials (Vibrant Frosted Translucent Colors + Glowing Wireframe)
    const colorIndigo = 0x4F46E5;
    const colorViolet = 0x8B5CF6;
    const colorCyan = 0x06B6D4;
    const colorRose = 0xEC4899;

    const materials = [
      new THREE.MeshStandardMaterial({
        color: colorIndigo,
        roughness: 0.2,
        metalness: 0.4,
        transparent: true,
        opacity: 0.55,
        flatShading: true
      }),
      new THREE.MeshStandardMaterial({
        color: colorViolet,
        roughness: 0.2,
        metalness: 0.4,
        transparent: true,
        opacity: 0.52,
        flatShading: true
      }),
      new THREE.MeshStandardMaterial({
        color: colorCyan,
        roughness: 0.15,
        metalness: 0.5,
        transparent: true,
        opacity: 0.48,
        flatShading: true
      }),
      new THREE.MeshStandardMaterial({
        color: colorRose,
        roughness: 0.25,
        metalness: 0.3,
        transparent: true,
        opacity: 0.45,
        flatShading: true
      })
    ];

    const wireframeMaterial = new THREE.MeshBasicMaterial({
      color: 0x4F46E5,
      wireframe: true,
      transparent: true,
      opacity: 0.40
    });

    // 5. Geometry Models (Icosahedrons, Torus, Octahedrons, Dodecahedrons)
    const geometries = [
      new THREE.IcosahedronGeometry(2.2, 0),
      new THREE.IcosahedronGeometry(2.8, 0),
      new THREE.DodecahedronGeometry(2.0, 0),
      new THREE.OctahedronGeometry(2.4, 0),
      new THREE.TorusGeometry(2.2, 0.65, 8, 18),
      new THREE.TorusGeometry(1.6, 0.45, 6, 14),
      new THREE.TetrahedronGeometry(2.6, 0)
    ];

    const isMobile = width < 768;
    const shapeCount = isMobile ? 14 : 32;

    for (let i = 0; i < shapeCount; i++) {
      const geom = geometries[Math.floor(Math.random() * geometries.length)];
      const mat = materials[Math.floor(Math.random() * materials.length)];

      const group = new THREE.Group();

      // Solid Shaded Mesh
      const mesh = new THREE.Mesh(geom, mat);
      group.add(mesh);

      // Glowing Wireframe Outline Mesh
      const wireMesh = new THREE.Mesh(geom, wireframeMaterial);
      wireMesh.scale.set(1.01, 1.01, 1.01);
      group.add(wireMesh);

      // Distribute in 3D Space
      group.position.x = (Math.random() - 0.5) * 65;
      group.position.y = (Math.random() - 0.5) * 48;
      group.position.z = (Math.random() - 0.5) * 28 - 2;

      group.rotation.x = Math.random() * Math.PI * 2;
      group.rotation.y = Math.random() * Math.PI * 2;
      group.rotation.z = Math.random() * Math.PI * 2;

      const scale = 0.7 + Math.random() * 0.7;
      group.scale.set(scale, scale, scale);

      shapes.push({
        group: group,
        rotSpeedX: (Math.random() - 0.5) * 0.009,
        rotSpeedY: (Math.random() - 0.5) * 0.011,
        rotSpeedZ: (Math.random() - 0.5) * 0.007,
        floatSpeed: 0.0009 + Math.random() * 0.0013,
        floatOffset: Math.random() * Math.PI * 2,
        floatAmplitude: 0.9 + Math.random() * 1.3,
        baseY: group.position.y
      });

      scene.add(group);
    }

    // 6. Ambient 3D Particle Starfield
    const particleCount = isMobile ? 60 : 160;
    const particleGeom = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      particlePositions[i] = (Math.random() - 0.5) * 85;
      particlePositions[i + 1] = (Math.random() - 0.5) * 65;
      particlePositions[i + 2] = (Math.random() - 0.5) * 45;
    }

    particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0x818CF8,
      size: 0.75,
      transparent: true,
      opacity: 0.70
    });

    particleSystem = new THREE.Points(particleGeom, particleMat);
    scene.add(particleSystem);

    // 7. Event Listeners
    if (!isMobile) {
      window.addEventListener('mousemove', onMouseMove, { passive: true });
    }
    window.addEventListener('resize', onWindowResize, { passive: true });
    document.addEventListener('visibilitychange', onVisibilityChange);

    // Initial render & loop start
    if (prefersReducedMotion) {
      renderer.render(scene, camera);
    } else {
      animate();
    }
  }

  function onMouseMove(event) {
    targetMouseX = (event.clientX / window.innerWidth - 0.5) * 3.5;
    targetMouseY = (event.clientY / window.innerHeight - 0.5) * 3.5;
  }

  function onWindowResize() {
    if (!camera || !renderer) return;
    const w = window.innerWidth;
    const h = window.innerHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
    if (prefersReducedMotion) {
      renderer.render(scene, camera);
    }
  }

  function onVisibilityChange() {
    isTabActive = !document.hidden;
    if (isTabActive && !prefersReducedMotion) {
      if (!animationFrameId) animate();
    } else {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
      }
    }
  }

  let time = 0;
  function animate() {
    if (!isTabActive || prefersReducedMotion) return;

    animationFrameId = requestAnimationFrame(animate);
    time += 1;

    // Smooth camera mouse parallax lerp
    mouseX += (targetMouseX - mouseX) * 0.05;
    mouseY += (targetMouseY - mouseY) * 0.05;

    camera.position.x = mouseX * 1.5;
    camera.position.y = -mouseY * 1.5;
    camera.lookAt(0, 0, 0);

    // Animate 3D shapes
    for (let i = 0; i < shapes.length; i++) {
      const s = shapes[i];
      s.group.rotation.x += s.rotSpeedX;
      s.group.rotation.y += s.rotSpeedY;
      s.group.rotation.z += s.rotSpeedZ;
      s.group.position.y = s.baseY + Math.sin(time * s.floatSpeed + s.floatOffset) * s.floatAmplitude;
    }

    // Animate background particles
    if (particleSystem) {
      particleSystem.rotation.y = time * 0.0003;
      particleSystem.rotation.x = time * 0.0002;
    }

    renderer.render(scene, camera);
  }

  // Auto initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init3DBackground);
  } else {
    init3DBackground();
  }
})();
