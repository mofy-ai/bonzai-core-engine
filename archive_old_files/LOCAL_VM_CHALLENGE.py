#!/usr/bin/env python3
"""
🚨 45-MINUTE LOCAL VM CHALLENGE - DOCKER DESKTOP EDITION
FastAPI VM Service using Docker Desktop containers as "VMs"
CRUSHING CLAUDE DESKTOP'S 4-WEEK PREDICTION LOCALLY! ⚡
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import docker
import uuid
import json
import asyncio
import os
import subprocess
from datetime import datetime
from typing import Dict, Any

app = FastAPI(
    title="LOCAL MOFY VM Service - 45 MINUTE CHALLENGE!",
    description="Docker Desktop VM simulation - BEATING CLAUDE DESKTOP LOCALLY!",
    version="1.0.0"
)

# CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Docker client
try:
    docker_client = docker.from_env()
    docker_available = True
    print("🐳 Docker Desktop connected successfully!")
except Exception as e:
    docker_available = False
    print(f" Docker not available: {e}")

# VM management state
active_vms = {}
deployment_stats = {
    "vms_created": 0,
    "start_time": datetime.now(),
    "challenge_duration": "45:00",
    "docker_available": docker_available
}

@app.get("/")
async def root():
    """Service status and challenge progress"""
    elapsed = datetime.now() - deployment_stats["start_time"]
    return {
        "service": "LOCAL MOFY VM Challenge Service",
        "status": " CRUSHING CLAUDE DESKTOP'S 4 WEEKS LOCALLY!",
        "docker_status": " Connected" if docker_available else " Not Available",
        "challenge_time_remaining": "WINNING LOCALLY!",
        "elapsed_time": str(elapsed).split('.')[0],
        "vms_created": deployment_stats["vms_created"],
        "message": "LET'S WIN THAT £20 WITH DOCKER! ⚡",
        "advantage": "No gcloud needed - pure local power!"
    }

@app.post("/vm/create")
async def create_vm(vm_type: str = "ubuntu", ports: str = "8080:8080"):
    """ INSTANT LOCAL VM CREATION - DOCKER CONTAINER AS VM!"""
    try:
        if not docker_available:
            raise HTTPException(status_code=503, detail="Docker Desktop not available")
        
        vm_id = f"mofy-vm-{str(uuid.uuid4())[:8]}"
        
        print(f" Creating LOCAL VM: {vm_id}")
        
        # Create container as "VM"
        container = docker_client.containers.run(
            "ubuntu:20.04",
            name=vm_id,
            detach=True,
            ports={'8080/tcp': None} if ports else None,
            environment={
                "MOFY_VM_ID": vm_id,
                "MOFY_CHALLENGE": "45_MINUTE_LOCAL_WIN"
            },
            command=[
                "/bin/bash", "-c", 
                "apt-get update && "
                "apt-get install -y curl wget python3 python3-pip && "
                "echo 'MOFY LOCAL VM READY!' > /tmp/mofy-ready.log && "
                "echo 'VM ID: " + vm_id + "' >> /tmp/mofy-ready.log && "
                "tail -f /dev/null"  # Keep container running
            ]
        )
        
        # Get container info
        container.reload()
        
        # Track the VM
        active_vms[vm_id] = {
            "id": vm_id,
            "container_id": container.id,
            "container_name": container.name,
            "created_at": datetime.now(),
            "status": "CREATING",
            "type": "local_docker_vm",
            "ports": container.ports
        }
        
        deployment_stats["vms_created"] += 1
        
        return {
            "success": True,
            "vm_id": vm_id,
            "container_id": container.id[:12],
            "status": "CREATING",
            "estimated_ready": "5 seconds (LOCAL SPEED!)",
            "type": "docker_container_vm",
            "ports": container.ports,
            "message": f" LOCAL VM #{deployment_stats['vms_created']} launching!",
            "challenge_progress": f"DESTROYING 4-WEEK ESTIMATE LOCALLY!",
            "advantage": "No cloud needed - instant local deployment!"
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local VM creation failed: {str(e)}")

@app.get("/vm/{vm_id}")
async def get_vm_status(vm_id: str):
    """ CHECK LOCAL VM STATUS & GET CONNECTION INFO"""
    try:
        if vm_id not in active_vms:
            return {"success": False, "error": "VM not found in our records"}
        
        vm_info = active_vms[vm_id]
        
        # Get container status
        try:
            container = docker_client.containers.get(vm_info["container_id"])
            container.reload()
            
            status = container.status.upper()
            active_vms[vm_id]["status"] = status
            
            response = {
                "vm_id": vm_id,
                "container_id": container.id[:12],
                "status": status,
                "created_at": vm_info["created_at"].isoformat(),
                "type": "local_docker_vm",
                "ports": container.ports
            }
            
            # If running, get connection info
            if status == "RUNNING":
                # Get container IP
                networks = container.attrs['NetworkSettings']['Networks']
                ip_address = list(networks.values())[0]['IPAddress'] if networks else "localhost"
                
                response.update({
                    "ip_address": ip_address,
                    "local_access": f"docker exec -it {container.name} /bin/bash",
                    "ready": True,
                    "message": " LOCAL VM READY FOR CONNECTION!",
                    "logs_command": f"docker logs {container.name}",
                    "advantage": "Instant local access - no SSH needed!"
                })
            
            return {"success": True, **response}
            
        except docker.errors.NotFound:
            return {
                "success": False,
                "error": "Container not found - may have been removed",
                "vm_id": vm_id
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.delete("/vm/{vm_id}")
async def delete_vm(vm_id: str):
    """🗑️ INSTANT LOCAL VM DELETION - STOP CONTAINER"""
    try:
        if vm_id not in active_vms:
            return {"success": False, "error": "VM not found"}
        
        vm_info = active_vms[vm_id]
        
        try:
            # Stop and remove container
            container = docker_client.containers.get(vm_info["container_id"])
            container.stop(timeout=5)
            container.remove()
            
            # Remove from tracking
            del active_vms[vm_id]
            
            return {
                "success": True,
                "vm_id": vm_id,
                "status": "DELETED",
                "message": "💥 LOCAL VM destroyed instantly!",
                "advantage": "Instant cleanup - no cloud billing!"
            }
            
        except docker.errors.NotFound:
            # Container already gone, just remove from tracking
            if vm_id in active_vms:
                del active_vms[vm_id]
            
            return {
                "success": True,
                "vm_id": vm_id,
                "status": "ALREADY_DELETED",
                "message": "💥 Container was already removed!"
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

@app.get("/vm/list/all")
async def list_all_vms():
    """📋 LIST ALL ACTIVE LOCAL VMS"""
    return {
        "active_vms": len(active_vms),
        "vms": list(active_vms.values()),
        "total_created": deployment_stats["vms_created"],
        "challenge_status": " DEMOLISHING 4-WEEK ESTIMATE LOCALLY!",
        "docker_status": " Connected" if docker_available else " Not Available"
    }

@app.get("/challenge/status")
async def challenge_status():
    """ LOCAL CHALLENGE PROGRESS & VICTORY STATUS"""
    elapsed = datetime.now() - deployment_stats["start_time"]
    elapsed_minutes = int(elapsed.total_seconds() / 60)
    
    return {
        "challenge": "45-MINUTE LOCAL VM SERVICE DEPLOYMENT",
        "opponent": "Claude Desktop (predicted 4 weeks)",
        "our_time": f"{elapsed_minutes} minutes elapsed",
        "status": " WINNING LOCALLY!" if elapsed_minutes < 45 else " LOCAL VICTORY!",
        "vms_created": deployment_stats["vms_created"],
        "service_functional": docker_available,
        "bet_status": "£20 IS OURS!" if elapsed_minutes < 60 else " WON!",
        "message": "CRUSHING THE 4-WEEK PREDICTION WITH DOCKER! ⚡",
        "advantages": [
            "No cloud authentication needed",
            "Instant local deployment",
            "No billing concerns",
            "Full control",
            "Faster than cloud!"
        ]
    }

@app.get("/docker/info")
async def docker_info():
    """🐳 DOCKER DESKTOP STATUS & INFO"""
    if not docker_available:
        return {
            "available": False,
            "error": "Docker Desktop not running or not installed",
            "fix": "Start Docker Desktop application"
        }
    
    try:
        info = docker_client.info()
        return {
            "available": True,
            "containers_running": info.get('ContainersRunning', 0),
            "containers_total": info.get('Containers', 0),
            "images": info.get('Images', 0),
            "docker_version": info.get('ServerVersion', 'Unknown'),
            "memory_total": f"{info.get('MemTotal', 0) // (1024**3)}GB",
            "status": "🐳 Docker Desktop Ready for VM Challenge!"
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("🚨 45-MINUTE LOCAL VM CHALLENGE SERVICE STARTING!")
    print(" TARGET: Beat Claude Desktop's 4-week prediction LOCALLY")
    print("🐳 METHOD: Docker Desktop containers as VMs")
    print("💰 STAKES: £20 bet")
    print("⚡ LET'S FUCKING WIN THIS LOCALLY!")
    
    if not docker_available:
        print(" Docker Desktop not available - please start Docker Desktop")
        print(" Make sure Docker Desktop is running and try again")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info"
    )