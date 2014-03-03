
//
//  DBQRViewController.m
//
//  from 学鸿 张 on 13-11-29.
//  Copyright (c) 2013年 Steven. All rights reserved.
//

#import "DBQRViewController.h"
#import "DBDemoViewController.h"

@interface DBQRViewController ()

@property (nonatomic, assign) int num;
@property (nonatomic, assign) BOOL upOrdown;
@property (nonatomic, assign) NSTimer * timer;

@end

@implementation DBQRViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    UILabel * intro = [[UILabel alloc] initWithFrame:CGRectMake(15, 40, 290, 50)];
    intro.backgroundColor = [UIColor clearColor];
    intro.numberOfLines =2;
    intro.textColor = [UIColor whiteColor];
    intro.text = @"请扫描二维码开始演示 ^O^";
    intro.textAlignment = NSTextAlignmentCenter;
    [self.view addSubview:intro];
    
    UILabel * quit = [[UILabel alloc] initWithFrame:CGRectMake(15, 440, 290, 50)];
    quit.backgroundColor = [UIColor clearColor];
    quit.numberOfLines =2;
    quit.textColor = [UIColor whiteColor];
    quit.text = @"开始演示后，两指双击退出演示";
    quit.textAlignment = NSTextAlignmentCenter;
    [self.view addSubview:quit];
    
    self.upOrdown = NO;
    self.num = 0;
    self.line = [[UIImageView alloc] initWithFrame:CGRectMake(50, 110, 220, 2)];
    self.line.image = [UIImage imageNamed:@"line.png"];
    [self.view addSubview:self.line];
    
    self.timer = [NSTimer scheduledTimerWithTimeInterval:.02
                                                  target:self selector:@selector(scanAnimation) userInfo:nil repeats:YES];
    
}
-(void)scanAnimation
{
    if (self.upOrdown == NO) {
        self.num ++;
        self.line.frame = CGRectMake(50, 110+2*self.num, 220, 2);
        if (2*self.num == 280) {
            self.upOrdown = YES;
        }
    }else {
        self.num --;
        self.line.frame = CGRectMake(50, 110+2*self.num, 220, 2);
        if (self.num == 0) {
            self.upOrdown = NO;
        }
    }
    
}

-(void)viewWillAppear:(BOOL)animated
{
    //NSLog(@"viewWillAppear");
    [self setupCamera];

}

- (void)setupCamera
{
    //NSLog(@"setupCarmera");
    // Device
    self.device = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
    
    // Input
    self.input = [AVCaptureDeviceInput deviceInputWithDevice:self.device error:nil];
    
    // Output
    self.output = [[AVCaptureMetadataOutput alloc] init];
    [self.output setMetadataObjectsDelegate:self queue:dispatch_get_main_queue()];
    
    //NSLog(@"device %@, input %@, output %@", self.device, self.input, self.output);
    
    // Session
    self.session = [[AVCaptureSession alloc] init];
    [self.session setSessionPreset:AVCaptureSessionPresetHigh];
    if ([self.session canAddInput:self.input])
    {
        [self.session addInput:self.input];
    }
    
    if ([self.session canAddOutput:self.output])
    {
        [self.session addOutput:self.output];
    }
    
    // AVMetadataObjectTypeQRCode
    self.output.metadataObjectTypes = @[AVMetadataObjectTypeQRCode];
    
    // Preview
    if (self.preview){
        [self.preview removeFromSuperlayer];
    }
    
    self.preview = [AVCaptureVideoPreviewLayer layerWithSession:self.session];
    self.preview.videoGravity = AVLayerVideoGravityResizeAspectFill;
    self.preview.frame = CGRectMake(20,110,280,280);
    
    [self.view.layer insertSublayer:self.preview atIndex:0];
    
    //NSLog(@"session %@, preview %@", self.session, self.preview);
    
    // Start
    [self.session startRunning];
    [self.timer setFireDate:[NSDate distantPast]];

}

#pragma mark AVCaptureMetadataOutputObjectsDelegate
- (void)captureOutput:(AVCaptureOutput *)captureOutput didOutputMetadataObjects:(NSArray *)metadataObjects
                fromConnection:(AVCaptureConnection *)connection
{
    
    NSString *stringValue;
    
    if ([metadataObjects count] > 0)
    {
        AVMetadataMachineReadableCodeObject * metadataObject = [metadataObjects objectAtIndex:0];
        stringValue = metadataObject.stringValue;
    }
    
    [self.session stopRunning];
    
    //[self.timer invalidate];
    [self.timer setFireDate:[NSDate distantFuture]];
    NSLog(@"scan url=%@",stringValue);
    DBDemoViewController * dc = [[DBDemoViewController alloc] initWithUrl:stringValue];
    [self.navigationController pushViewController:dc animated:YES];
    
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
