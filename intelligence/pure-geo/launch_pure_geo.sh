#!/bin/bash

# 🌍 Pure GEO - AI Geolocalization Intelligence System
# Launch script for Pure GEO operations

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Pure GEO Banner
echo -e "${BLUE}"
echo "  ██████╗ ██╗   ██╗██████╗ ███████╗     ██████╗ ███████╗ ██████╗ "
echo "  ██╔══██╗██║   ██║██╔══██╗██╔════╝    ██╔════╝ ██╔════╝██╔═══██╗"
echo "  ██████╔╝██║   ██║██████╔╝█████╗      ██║  ███╗█████╗  ██║   ██║"
echo "  ██╔═══╝ ██║   ██║██╔══██╗██╔══╝      ██║   ██║██╔══╝  ██║   ██║"
echo "  ██║     ╚██████╔╝██║  ██║███████╗    ╚██████╔╝███████╗╚██████╔╝"
echo "  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${CYAN}    Advanced AI Geolocalization Intelligence System${NC}"
echo -e "${PURPLE}    Precision Geography through Artificial Intelligence${NC}"
echo ""

# Check if we're in the right directory
if [[ ! -f "main.py" || ! -d "src" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the Pure GEO directory${NC}"
    exit 1
fi

# Function to display menu
show_menu() {
    echo -e "${YELLOW}🎯 Pure GEO Operations Menu:${NC}"
    echo "1. 📸 Analyze Single Image"
    echo "2. 🧪 Run Test Suite"
    echo "3. 🏋️  Train Production Model"
    echo "4. 📊 Batch Process Images"
    echo "5. 🔧 System Status Check"
    echo "6. 📖 View Documentation"
    echo "7. 🚪 Exit"
    echo ""
}

# Function to analyze single image
analyze_image() {
    echo -e "${GREEN}📸 Pure GEO Image Analysis${NC}"
    echo ""
    
    # Check for mission.jpg first
    if [[ -f "/home/xx/Desktop/mission.jpg" ]]; then
        echo -e "${CYAN}Found mission.jpg on Desktop. Analyze this image? (y/n):${NC}"
        read -r response
        if [[ "$response" == "y" || "$response" == "Y" ]]; then
            IMAGE_PATH="/home/xx/Desktop/mission.jpg"
        fi
    fi
    
    # If no image selected, prompt for path
    if [[ -z "$IMAGE_PATH" ]]; then
        echo -e "${CYAN}Enter image path:${NC}"
        read -r IMAGE_PATH
    fi
    
    if [[ ! -f "$IMAGE_PATH" ]]; then
        echo -e "${RED}❌ Image file not found: $IMAGE_PATH${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🔍 Analyzing image: $IMAGE_PATH${NC}"
    echo ""
    
    # Run Pure GEO analysis
    python predict.py \
        --model trained_models/best_model.pth \
        --data-dir processed_data \
        --image "$IMAGE_PATH" \
        --config configs/production_config.yaml \
        --output pure_geo_analysis.json
    
    echo ""
    echo -e "${GREEN}✅ Analysis complete! Results saved to pure_geo_analysis.json${NC}"
}

# Function to run test suite
run_tests() {
    echo -e "${GREEN}🧪 Pure GEO Test Suite${NC}"
    echo ""
    
    # Run integration tests
    python test_integration.py
    
    # Run terrain tests if available
    if [[ -d "additional_test_images" ]]; then
        echo ""
        echo -e "${BLUE}🏞️  Testing terrain classification...${NC}"
        
        for terrain in beach desert forest mountain urban; do
            if [[ -f "additional_test_images/test_${terrain}.jpg" ]]; then
                echo -e "${CYAN}Testing ${terrain} image...${NC}"
                python predict.py \
                    --model trained_models/best_model.pth \
                    --data-dir processed_data \
                    --image "additional_test_images/test_${terrain}.jpg" \
                    --config configs/test_config.yaml \
                    --output "results_${terrain}_test.json" > /dev/null 2>&1
                
                if [[ $? -eq 0 ]]; then
                    echo -e "${GREEN}✅ ${terrain} test passed${NC}"
                else
                    echo -e "${RED}❌ ${terrain} test failed${NC}"
                fi
            fi
        done
    fi
    
    echo ""
    echo -e "${GREEN}✅ Test suite completed${NC}"
}

# Function to train model
train_model() {
    echo -e "${GREEN}🏋️  Pure GEO Model Training${NC}"
    echo ""
    echo -e "${YELLOW}Select training configuration:${NC}"
    echo "1. Quick Test Training (5 epochs)"
    echo "2. Balanced Training (50 epochs)"
    echo "3. Production Training (150 epochs)"
    echo ""
    
    read -r training_choice
    
    case $training_choice in
        1)
            CONFIG="configs/test_config.yaml"
            echo -e "${BLUE}Starting quick test training...${NC}"
            ;;
        2)
            CONFIG="configs/optimized_config.yaml" 
            echo -e "${BLUE}Starting balanced training...${NC}"
            ;;
        3)
            CONFIG="configs/production_config.yaml"
            echo -e "${BLUE}Starting production training...${NC}"
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            return 1
            ;;
    esac
    
    # Start training
    python main.py \
        --config "$CONFIG" \
        --data-source custom \
        --data-path data/datasets/train_dataset.csv \
        --max-images 1000
}

# Function to process batch images
batch_process() {
    echo -e "${GREEN}📊 Pure GEO Batch Processing${NC}"
    echo ""
    echo -e "${CYAN}Enter directory containing images:${NC}"
    read -r BATCH_DIR
    
    if [[ ! -d "$BATCH_DIR" ]]; then
        echo -e "${RED}❌ Directory not found: $BATCH_DIR${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🔍 Processing images in: $BATCH_DIR${NC}"
    echo ""
    
    # Count images
    IMAGE_COUNT=$(find "$BATCH_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l)
    echo -e "${CYAN}Found $IMAGE_COUNT images to process${NC}"
    
    if [[ $IMAGE_COUNT -eq 0 ]]; then
        echo -e "${RED}❌ No images found in directory${NC}"
        return 1
    fi
    
    # Process each image
    PROCESSED=0
    find "$BATCH_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r image; do
        basename_image=$(basename "$image")
        echo -e "${CYAN}Processing: $basename_image${NC}"
        
        python predict.py \
            --model trained_models/best_model.pth \
            --data-dir processed_data \
            --image "$image" \
            --config configs/production_config.yaml \
            --output "batch_results_${basename_image%.*}.json" > /dev/null 2>&1
        
        ((PROCESSED++))
        echo -e "${GREEN}✅ Processed $PROCESSED/$IMAGE_COUNT images${NC}"
    done
    
    echo ""
    echo -e "${GREEN}✅ Batch processing completed${NC}"
}

# Function to check system status
system_status() {
    echo -e "${GREEN}🔧 Pure GEO System Status${NC}"
    echo ""
    
    # Check Python environment
    echo -e "${CYAN}🐍 Python Environment:${NC}"
    python --version
    echo ""
    
    # Check dependencies
    echo -e "${CYAN}📦 Key Dependencies:${NC}"
    python -c "import torch; print(f'PyTorch: {torch.__version__}')" 2>/dev/null || echo "❌ PyTorch not found"
    python -c "import torchvision; print(f'TorchVision: {torchvision.__version__}')" 2>/dev/null || echo "❌ TorchVision not found"
    python -c "import PIL; print(f'Pillow: {PIL.__version__}')" 2>/dev/null || echo "❌ Pillow not found"
    python -c "import pandas as pd; print(f'Pandas: {pd.__version__}')" 2>/dev/null || echo "❌ Pandas not found"
    echo ""
    
    # Check models
    echo -e "${CYAN}🧠 Model Status:${NC}"
    if [[ -f "trained_models/best_model.pth" ]]; then
        MODEL_SIZE=$(du -h trained_models/best_model.pth | cut -f1)
        echo -e "${GREEN}✅ Main model available ($MODEL_SIZE)${NC}"
    else
        echo -e "${RED}❌ Main model not found${NC}"
    fi
    echo ""
    
    # Check data
    echo -e "${CYAN}📊 Data Status:${NC}"
    if [[ -f "processed_data/dataset.csv" ]]; then
        DATA_LINES=$(wc -l < processed_data/dataset.csv)
        echo -e "${GREEN}✅ Processed data available ($DATA_LINES rows)${NC}"
    else
        echo -e "${RED}❌ Processed data not found${NC}"
    fi
    
    if [[ -d "data/datasets" ]]; then
        DATASET_COUNT=$(find data/datasets -name "*.csv" | wc -l)
        echo -e "${GREEN}✅ Training datasets available ($DATASET_COUNT files)${NC}"
    else
        echo -e "${RED}❌ Training datasets not found${NC}"
    fi
    echo ""
    
    # Check configurations
    echo -e "${CYAN}⚙️ Configuration Status:${NC}"
    for config in configs/*.yaml; do
        if [[ -f "$config" ]]; then
            config_name=$(basename "$config")
            echo -e "${GREEN}✅ $config_name${NC}"
        fi
    done
    echo ""
}

# Function to view documentation
view_docs() {
    echo -e "${GREEN}📖 Pure GEO Documentation${NC}"
    echo ""
    
    if [[ -f "README.md" ]]; then
        echo -e "${CYAN}Opening README.md...${NC}"
        less README.md
    else
        echo -e "${RED}❌ Documentation not found${NC}"
    fi
}

# Main menu loop
while true; do
    show_menu
    echo -e "${CYAN}Select an option (1-7):${NC}"
    read -r choice
    echo ""
    
    case $choice in
        1)
            analyze_image
            ;;
        2)
            run_tests
            ;;
        3)
            train_model
            ;;
        4)
            batch_process
            ;;
        5)
            system_status
            ;;
        6)
            view_docs
            ;;
        7)
            echo -e "${GREEN}🌍 Thanks for using Pure GEO! Goodbye! ✨${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid option. Please select 1-7.${NC}"
            ;;
    esac
    
    echo ""
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read -r
    echo ""
done