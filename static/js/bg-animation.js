/**
 * ResumeForge AI — Subtle, Refined 3D Ambient Background (Three.js r128)
 * Clean, lightweight, sparse floating crystal geometry placed around edges to avoid text clutter.
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

    // Fixed background canvas behind content
    canvas.style.position = 'fixed';
    canvas.style.top = '0px';
    canvas.style.left = '0px';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';
    canvas.style.display = 'block';

    if (typeof THREE === 'undefined') {
      return;
    }

    prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 1. Scene & Camera Setup (Camera pushed further back for spacious feel)
    scene = new THREE.Scene();
    const width = window.innerWidth;
    const height = window.innerHeight;

    camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.z = 40;

    // 2. WebGL Renderer
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'low-power'
    });
    renderer.setSize(width, height, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

    // 3. Ambient & Point Lighting (Soft & gentle)
    const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.85);
    scene.add(ambientLight);

    const pointLightPrimary = new THREE.PointLight(0x4F46E5, 1.5, 90);
    pointLightPrimary.position.set(30, 25, 20);
    scene.add(pointLightPrimary);

    const pointLightSecondary = new THREE.PointLight(0x8B5CF6, 1.2, 90);
    pointLightSecondary.position.set(-30, -20, 15);
    scene.add(pointLightSecondary);

    // 4. Subtle, Low-Opacity Materials (0.18 - 0.22 opacity so text is 100% legible)
    const materials = [
      new THREE.MeshStandardMaterial({
        color: 0x4F46E5,
        roughness: 0.3,
        metalness: 0.2,
        transparent: true,
        opacity: 0.22,
        flatShading: true
      }),
      new THREE.MeshStandardMaterial({
        color: 0x8B5CF6,
        roughness: 0.3,
        metalness: 0.2,
        transparent: true,
        opacity: 0.20,
        flatShading: true
      }),
      new THREE.MeshStandardMaterial({
        color: 0x06B6D4,
        roughness: 0.25,
        metalness: 0.3,
        transparent: true,
        opacity: 0.18,
        flatShading: true
      })
    ];

    const wireframeMaterial = new THREE.MeshBasicMaterial({
      color: 0x818CF8,
      wireframe: true,
      transparent: true,
      opacity: 0.16
    });

    // 5. Refined Geometric Shapes (Smaller scale)
    const geometries = [
      new THREE.IcosahedronGeometry(1.4, 0),
      new THREE.IcosahedronGeometry(1.8, 0),
      new THREE.DodecahedronGeometry(1.3, 0),
      new THREE.OctahedronGeometry(1.5, 0),
      new THREE.TorusGeometry(1.4, 0.35, 8, 16)
    ];

    // Reduced mesh count: Only 10-12 shapes on desktop, 6 on mobile
    const isMobile = width < 768;
    const shapeCount = isMobile ? 6 : 12;

    for (let i = 0; i < shapeCount; i++) {
      const geom = geometries[Math.floor(Math.random() * geometries.length)];
      const mat = materials[Math.floor(Math.random() * materials.length)];

      const group = new THREE.Group();

      const mesh = new THREE.Mesh(geom, mat);
      group.add(mesh);

      const wireMesh = new THREE.Mesh(geom, wireframeMaterial);
      wireMesh.scale.set(1.01, 1.01, 1.01);
      group.add(wireMesh);

      // Keep shapes mostly towards edges and periphery to leave center text crystal clear
      const angle = (i / shapeCount) * Math.PI * 2 + (Math.random() * 0.4);
      const radiusX = 22 + Math.random() * 14;
      const radiusY = 14 + Math.random() * 10;

      group.position.x = Math.cos(angle) * radiusX;
      group.position.y = Math.sin(angle) * radiusY;
      group.position.z = (Math.random() - 0.5) * 15 - 4;

      group.rotation.x = Math.random() * Math.PI * 2;
      group.rotation.y = Math.random() * Math.PI * 2;
      group.rotation.z = Math.random() * Math.PI * 2;

      const scale = 0.55 + Math.random() * 0.45;
      group.scale.set(scale, scale, scale);

      shapes.push({
        group: group,
        rotSpeedX: (Math.random() - 0.5) * 0.005,
        rotSpeedY: (Math.random() - 0.5) * 0.006,
        rotSpeedZ: (Math.random() - 0.5) * 0.004,
        floatSpeed: 0.0006 + Math.random() * 0.0008,
        floatOffset: Math.random() * Math.PI * 2,
        floatAmplitude: 0.5 + Math.random() * 0.6,
        baseY: group.position.y
      });

      scene.add(group);
    }

    // 6. Subtle Ambient Starfield (Tiny and soft)
    const particleCount = isMobile ? 30 : 60;
    const particleGeom = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      particlePositions[i] = (Math.random() - 0.5) * 75;
      particlePositions[i + 1] = (Math.random() - 0.5) * 55;
      particlePositions[i + 2] = (Math.random() - 0.5) * 30;
    }

    particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0x818CF8,
      size: 0.45,
      transparent: true,
      opacity: 0.45
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
    targetMouseX = (event.clientX / window.innerWidth - 0.5) * 2.0;
    targetMouseY = (event.clientY / window.innerHeight - 0.5) * 2.0;
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

    // Smooth subtle camera mouse parallax
    mouseX += (targetMouseX - mouseX) * 0.03;
    mouseY += (targetMouseY - mouseY) * 0.03;

    camera.position.x = mouseX * 1.0;
    camera.position.y = -mouseY * 1.0;
    camera.lookAt(0, 0, 0);

    for (let i = 0; i < shapes.length; i++) {
      const s = shapes[i];
      s.group.rotation.x += s.rotSpeedX;
      s.group.rotation.y += s.rotSpeedY;
      s.group.rotation.z += s.rotSpeedZ;
      s.group.position.y = s.baseY + Math.sin(time * s.floatSpeed + s.floatOffset) * s.floatAmplitude;
    }

    if (particleSystem) {
      particleSystem.rotation.y = time * 0.0002;
    }

    renderer.render(scene, camera);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init3DBackground);
  } else {
    init3DBackground();
  }
})();
