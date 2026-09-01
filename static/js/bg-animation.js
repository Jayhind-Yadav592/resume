/**
 * ResumeForge AI — Lightweight 3D Animated Background (Three.js r128)
 * Features low-poly floating geometry, subtle brand glow, parallax, and zero CPU waste.
 */

(function () {
  'use strict';

  let scene, camera, renderer, animationFrameId;
  let shapes = [];
  let mouseX = 0, mouseY = 0;
  let targetMouseX = 0, targetMouseY = 0;
  let isTabActive = true;
  let prefersReducedMotion = false;
  const canvasId = 'bg-canvas';

  function initThreeBackground() {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof THREE === 'undefined') {
      return;
    }

    // Check prefers-reduced-motion
    prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 1. Scene Setup
    scene = new THREE.Scene();

    const width = window.innerWidth;
    const height = window.innerHeight;

    // 2. Camera Setup
    camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.z = 32;

    // 3. Renderer Setup
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'low-power'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

    // 4. Lighting (Soft, subtle shaded shapes)
    const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.85);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x818CF8, 1.2, 80);
    pointLight.position.set(20, 20, 20);
    scene.add(pointLight);

    const pointLight2 = new THREE.PointLight(0x4F46E5, 0.9, 80);
    pointLight2.position.set(-20, -20, 15);
    scene.add(pointLight2);

    // 5. Materials (Brand Indigo & Soft Violet at 0.15-0.22 opacity)
    const indigoColor = new THREE.Color(0x4F46E5);
    const violetColor = new THREE.Color(0x818CF8);

    const materialIndigo = new THREE.MeshStandardMaterial({
      color: indigoColor,
      roughness: 0.35,
      metalness: 0.15,
      transparent: true,
      opacity: 0.18,
      flatShading: true
    });

    const materialViolet = new THREE.MeshStandardMaterial({
      color: violetColor,
      roughness: 0.35,
      metalness: 0.15,
      transparent: true,
      opacity: 0.20,
      flatShading: true
    });

    // 6. Geometry Generation (25-35 on desktop, 10-12 on mobile)
    const isMobile = width < 768;
    const shapeCount = isMobile ? 12 : 28;

    const geometries = [
      new THREE.IcosahedronGeometry(1.6, 0),
      new THREE.IcosahedronGeometry(2.4, 0),
      new THREE.TorusGeometry(1.8, 0.5, 8, 16),
      new THREE.TorusGeometry(1.2, 0.35, 6, 12),
      new THREE.OctahedronGeometry(1.8, 0)
    ];

    for (let i = 0; i < shapeCount; i++) {
      const geom = geometries[Math.floor(Math.random() * geometries.length)];
      const mat = (i % 2 === 0) ? materialIndigo : materialViolet;
      const mesh = new THREE.Mesh(geom, mat);

      // Random 3D space distribution
      mesh.position.x = (Math.random() - 0.5) * 55;
      mesh.position.y = (Math.random() - 0.5) * 38;
      mesh.position.z = (Math.random() - 0.5) * 25 - 5;

      // Random rotation
      mesh.rotation.x = Math.random() * Math.PI * 2;
      mesh.rotation.y = Math.random() * Math.PI * 2;
      mesh.rotation.z = Math.random() * Math.PI * 2;

      // Unique gentle drift and rotation attributes
      const shapeData = {
        mesh: mesh,
        rotSpeedX: (Math.random() - 0.5) * 0.006,
        rotSpeedY: (Math.random() - 0.5) * 0.008,
        rotSpeedZ: (Math.random() - 0.5) * 0.005,
        floatSpeed: 0.0008 + Math.random() * 0.0012,
        floatOffset: Math.random() * Math.PI * 2,
        floatAmplitude: 0.6 + Math.random() * 0.8,
        baseY: mesh.position.y
      };

      shapes.push(shapeData);
      scene.add(mesh);
    }

    // 7. Event Listeners
    if (!isMobile) {
      window.addEventListener('mousemove', onMouseMove, { passive: true });
    }
    window.addEventListener('resize', onWindowResize, { passive: true });
    document.addEventListener('visibilitychange', onVisibilityChange);

    // Initial render / Start loop
    if (prefersReducedMotion) {
      renderer.render(scene, camera);
    } else {
      animate();
    }
  }

  function onMouseMove(event) {
    targetMouseX = (event.clientX / window.innerWidth - 0.5) * 2.5;
    targetMouseY = (event.clientY / window.innerHeight - 0.5) * 2.5;
  }

  function onWindowResize() {
    if (!camera || !renderer) return;
    const w = window.innerWidth;
    const h = window.innerHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
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

    // Smooth mouse parallax lerp
    mouseX += (targetMouseX - mouseX) * 0.04;
    mouseY += (targetMouseY - mouseY) * 0.04;

    camera.position.x = mouseX * 1.5;
    camera.position.y = -mouseY * 1.5;
    camera.lookAt(0, 0, 0);

    // Animate individual shapes
    for (let i = 0; i < shapes.length; i++) {
      const s = shapes[i];
      s.mesh.rotation.x += s.rotSpeedX;
      s.mesh.rotation.y += s.rotSpeedY;
      s.mesh.rotation.z += s.rotSpeedZ;
      s.mesh.position.y = s.baseY + Math.sin(time * s.floatSpeed + s.floatOffset) * s.floatAmplitude;
    }

    renderer.render(scene, camera);
  }

  // Cleanup helper
  window.destroyThreeBackground = function () {
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
    }
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('resize', onWindowResize);
    document.removeEventListener('visibilitychange', onVisibilityChange);

    if (scene) {
      shapes.forEach(s => {
        if (s.mesh.geometry) s.mesh.geometry.dispose();
        if (s.mesh.material) s.mesh.material.dispose();
        scene.remove(s.mesh);
      });
      shapes = [];
    }
    if (renderer) {
      renderer.dispose();
    }
  };

  // Safe DOMContentLoaded hook
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThreeBackground);
  } else {
    initThreeBackground();
  }
})();
