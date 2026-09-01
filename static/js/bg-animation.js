/**
 * ResumeForge AI — Subtle 3D Ambient Geometric Background (Three.js r128)
 * Fixed background layer with zero DOM obstruction, low CPU usage, and high aesthetics.
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

    // Force strict fixed background positioning
    canvas.style.setProperty('position', 'fixed', 'important');
    canvas.style.setProperty('top', '0px', 'important');
    canvas.style.setProperty('left', '0px', 'important');
    canvas.style.setProperty('width', '100vw', 'important');
    canvas.style.setProperty('height', '100vh', 'important');
    canvas.style.setProperty('z-index', '-9999', 'important');
    canvas.style.setProperty('pointer-events', 'none', 'important');
    canvas.style.setProperty('display', 'block', 'important');

    // Check accessibility reduced-motion preference
    prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 1. Scene Setup
    scene = new THREE.Scene();

    const width = window.innerWidth;
    const height = window.innerHeight;

    // 2. Camera Setup (Pushed further back for depth and subtler size)
    camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.z = 45;

    // 3. Renderer Setup
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'low-power'
    });
    renderer.setSize(width, height, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

    // 4. Soft Ambient Lighting
    const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.9);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x818CF8, 1.0, 100);
    pointLight.position.set(25, 30, 25);
    scene.add(pointLight);

    const pointLight2 = new THREE.PointLight(0x4F46E5, 0.8, 100);
    pointLight2.position.set(-25, -20, 20);
    scene.add(pointLight2);

    // 5. Materials (Brand Indigo & Soft Violet at subtle 0.10 - 0.14 opacity)
    const materialIndigo = new THREE.MeshStandardMaterial({
      color: 0x4F46E5,
      roughness: 0.4,
      metalness: 0.1,
      transparent: true,
      opacity: 0.12,
      flatShading: true
    });

    const materialViolet = new THREE.MeshStandardMaterial({
      color: 0x818CF8,
      roughness: 0.4,
      metalness: 0.1,
      transparent: true,
      opacity: 0.14,
      flatShading: true
    });

    // 6. Geometry Generation (Compact, refined particle size)
    const isMobile = width < 768;
    const shapeCount = isMobile ? 10 : 24;

    const geometries = [
      new THREE.IcosahedronGeometry(1.0, 0),
      new THREE.IcosahedronGeometry(1.4, 0),
      new THREE.TorusGeometry(1.2, 0.3, 8, 16),
      new THREE.TorusGeometry(0.9, 0.25, 6, 12),
      new THREE.OctahedronGeometry(1.1, 0)
    ];

    for (let i = 0; i < shapeCount; i++) {
      const geom = geometries[Math.floor(Math.random() * geometries.length)];
      const mat = (i % 2 === 0) ? materialIndigo : materialViolet;
      const mesh = new THREE.Mesh(geom, mat);

      // Distribute evenly across viewport
      mesh.position.x = (Math.random() - 0.5) * 70;
      mesh.position.y = (Math.random() - 0.5) * 50;
      mesh.position.z = (Math.random() - 0.5) * 30 - 5;

      mesh.rotation.x = Math.random() * Math.PI * 2;
      mesh.rotation.y = Math.random() * Math.PI * 2;
      mesh.rotation.z = Math.random() * Math.PI * 2;

      const shapeData = {
        mesh: mesh,
        rotSpeedX: (Math.random() - 0.5) * 0.004,
        rotSpeedY: (Math.random() - 0.5) * 0.005,
        rotSpeedZ: (Math.random() - 0.5) * 0.003,
        floatSpeed: 0.0006 + Math.random() * 0.0008,
        floatOffset: Math.random() * Math.PI * 2,
        floatAmplitude: 0.4 + Math.random() * 0.6,
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

    // Initial render
    if (prefersReducedMotion) {
      renderer.render(scene, camera);
    } else {
      animate();
    }
  }

  function onMouseMove(event) {
    targetMouseX = (event.clientX / window.innerWidth - 0.5) * 1.5;
    targetMouseY = (event.clientY / window.innerHeight - 0.5) * 1.5;
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

    // Smooth subtle camera lerp
    mouseX += (targetMouseX - mouseX) * 0.03;
    mouseY += (targetMouseY - mouseY) * 0.03;

    camera.position.x = mouseX * 1.2;
    camera.position.y = -mouseY * 1.2;
    camera.lookAt(0, 0, 0);

    for (let i = 0; i < shapes.length; i++) {
      const s = shapes[i];
      s.mesh.rotation.x += s.rotSpeedX;
      s.mesh.rotation.y += s.rotSpeedY;
      s.mesh.rotation.z += s.rotSpeedZ;
      s.mesh.position.y = s.baseY + Math.sin(time * s.floatSpeed + s.floatOffset) * s.floatAmplitude;
    }

    renderer.render(scene, camera);
  }

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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThreeBackground);
  } else {
    initThreeBackground();
  }
})();
